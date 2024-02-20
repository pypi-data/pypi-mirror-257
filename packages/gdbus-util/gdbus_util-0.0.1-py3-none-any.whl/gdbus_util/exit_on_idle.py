# SPDX-FileCopyrightText: © 2024 Adrian Dombeck <adrian.dombeck@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import signal
import threading
from enum import Enum
from typing import Optional, Callable

from gi.repository import GLib
from gi.repository import Gio
import systemd.daemon

logger = logging.getLogger(__package__)

maincontext = GLib.MainContext().default()


class State(Enum):
    RUNNING = 0
    FLUSHING = 1
    EXITING = 2


class ExitOnIdleService:
    def __init__(self, connection: Gio.DBusConnection, name: str, timeout: int) -> None:
        self.connection = connection
        self.name = name
        self.timeout = timeout
        self._state: State = State.RUNNING
        self._idle_timeout_source: Optional[GLib.Source] = None
        self._idle_timer_lock = threading.Lock()
        self._acquired_name = False

    def check_idle(self) -> bool:
        """Check if the service is idle. This method should be overridden
        by the subclass."""
        return True

    def on_name_acquired(self, connection: Gio.DBusConnection, name: str) -> None:
        logger.info(f"Acquired name {name} on the system bus")
        self._acquired_name = True

    def on_name_lost(self, connection: Gio.DBusConnection, name: str) -> None:
        if not self._acquired_name:
            logger.error(f"Failed to acquire name {name} on the system bus")
        else:
            logger.info(f"Lost name {name} on the system bus, terminating...")
        self.flush_and_exit()

    def flush_and_exit(self) -> None:
        self._state = State.FLUSHING
        maincontext.wakeup()

    def reset_idle_timer(self) -> None:
        # Take a lock to ensure that any timeout source that was created
        # is destroyed before we create a new one.
        with self._idle_timer_lock:
            if self._state != State.RUNNING:
                return

            if self._idle_timeout_source:
                self._idle_timeout_source.destroy()

            self._idle_timeout_source = GLib.timeout_source_new_seconds(self.timeout)
            self._idle_timeout_source.set_callback(self._on_idle_timer_expiration)
            self._idle_timeout_source.attach(maincontext)

    def _on_idle_timer_expiration(self, user_data=None) -> None:
        if self._state != State.RUNNING:
            logger.debug(f"Ignoring idle timer expiration, state is {self._state}")
            return

        if not self.check_idle():
            logger.debug("Idle timer expired, but not idle, resetting...")
            self.reset_idle_timer()
            return

        logger.info("Idle timer expired, flushing and exiting...")
        self.flush_and_exit()

    def _on_bus_name_released(
        self, bus: Gio.DBusConnection, res: Gio.AsyncResult = None
    ) -> None:
        logger.debug("Bus name released")
        self._state = State.EXITING
        maincontext.wakeup()

    def _on_sigterm(self, sig, frame):
        logger.info("Received SIGTERM, flushing and exiting...")
        self.flush_and_exit()

    def run(self) -> None:
        bus_id = Gio.bus_own_name_on_connection(
            self.connection,
            self.name,
            Gio.BusNameOwnerFlags.ALLOW_REPLACEMENT | Gio.BusNameOwnerFlags.REPLACE,
            self.on_name_acquired,
            self.on_name_lost,
        )

        signal.signal(signal.SIGTERM, self._on_sigterm)

        logger.debug("Entering main loop")

        logger.debug("Setting idle timer to %d seconds", self.timeout)
        self.reset_idle_timer()

        # Run the main loop until we are asked to exit
        while self._state == State.RUNNING:
            maincontext.iteration()

        logger.debug("Preparing to exit...")

        # Inform the service manager that we are going down, so that it
        # will queue all further start requests, instead of assuming we
        # are still running.
        # See https://github.com/systemd/systemd/blob/4931b8e471438abbc44d/src/shared/bus-util.c#L131
        systemd.daemon.notify("STOPPING=1")

        # Unregister the name and wait for the NameOwnerChanged signal.
        # We do this in order to make sure that any queued requests are
        # still processed before we really exit.
        # See https://github.com/systemd/systemd/blob/4931b8e471438abbc44d/src/shared/bus-util.c#L67
        match = (
            f"sender='org.freedesktop.DBus',"
            f"type='signal',"
            f"interface='org.freedesktop.DBus',"
            f"member='NameOwnerChanged'"
            f"path='/org/freedesktop/DBus'"
            f"arg0='{self.name}'"
            f"arg1='{self.connection.get_unique_name()}'"
            f"arg2=''"
        )
        self.connection.call(
            "org.freedesktop.DBus",
            "/org/freedesktop/DBus",
            "org.freedesktop.DBus",
            "AddMatch",
            GLib.Variant("(s)", (match,)),
            GLib.VariantType.new("u"),
            Gio.DBusCallFlags.NONE,
            -1,
            None,
            self._on_bus_name_released,
        )

        # systemd will send us a SIGTERM once we release the bus name
        # (assuming that we're running as a type=dbus systemd service),
        # so we ignore SIGTERM for the remainder of the shutdown process.
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        Gio.bus_unown_name(bus_id)

        # Keep iterating the main context to ensure that any queued
        # requests are still processed before we really exit.
        logger.debug("Flushing main context...")
        while self._state == State.FLUSHING:
            maincontext.iteration()

        logger.info("Exiting")
