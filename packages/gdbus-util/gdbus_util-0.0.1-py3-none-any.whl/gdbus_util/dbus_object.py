# SPDX-FileCopyrightText: © 2024 Adrian Dombeck <adrian.dombeck@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import cProfile
import logging
import pstats
import subprocess
import tempfile
import threading
from abc import abstractmethod, ABCMeta
import inspect
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Optional
from threading import Thread

from gi.repository import Gio, GLib

from .error import DBusError
from .exit_on_idle import ExitOnIdleService

logger = logging.getLogger(__package__)

PROFILING = False
PROFILES_DIR: Optional[str] = None


class RegistrationFailedError(Exception):
    pass


class UnregistrationFailedError(Exception):
    pass


class DBusObject(metaclass=ABCMeta):
    """DBusObject is an abstract class which facilitates registering
    D-Bus objects"""

    @property
    @abstractmethod
    def dbus_info(self) -> str:
        pass

    @property
    @abstractmethod
    def dbus_path(self) -> str:
        pass

    def __init__(self, connection: Gio.DBusConnection):
        if isinstance(self, ExitOnIdleService):
            self.exit_on_idle_service = self
        else:
            self.exit_on_idle_service = None

        self.connection = connection
        self.registered = False
        self.num_ongoing_calls = 0

        self._node_info = Gio.DBusNodeInfo.new_for_xml(self.dbus_info)
        self._reg_ids = list()
        self._num_ongoing_calls_lock = threading.Lock()

        # Create a dictionary of signals and their arguments for easy lookup
        self._signals = dict()
        for interface in self._node_info.interfaces:
            for signal in interface.signals:
                args = {arg.name: arg.signature for arg in signal.args}
                self._signals[signal.name] = {"interface": interface.name, "args": args}

        """Register the DBus interfaces of this object"""
        logger.debug("Registering %s", self.dbus_path)

        for interface in self._node_info.interfaces:
            reg_id = connection.register_object(
                self.dbus_path,
                interface,
                self._handle_method_call_async,
                self._handle_get_property,
                self._handle_set_property,
            )
            if not reg_id:
                raise RegistrationFailedError(
                    f"Failed to register interface {interface} of object {self}"
                )

            # Store the registration id so that we can unregister the
            # interfaces in the self.unregister method
            self._reg_ids.append(reg_id)

        self.registered = True

    def unregister(self, connection: Gio.DBusConnection):
        logger.debug("Unregistering %r", self.dbus_path)
        for reg_id in self._reg_ids:
            unregistered = connection.unregister_object(reg_id)
            if not unregistered:
                raise UnregistrationFailedError("Failed to unregister object %r" % self)
        self._reg_ids = list()
        self.registered = False

    def emit_signal(self, signal_name: str, values: dict[str, Any]):
        signal = self._signals[signal_name]
        parameters = []
        for arg_name, arg_signature in signal["args"].items():
            value = values[arg_name]
            parameters.append(GLib.Variant(arg_signature, value))

        variant = GLib.Variant.new_tuple(*parameters)
        self.connection.emit_signal(
            None,
            self.dbus_path,
            signal["interface"],
            signal_name,
            variant,
        )

    def emit_properties_changed_signal(
        self,
        interface_name: str,
        changed_properties: dict[str, GLib.Variant],
        invalidated_properties: Optional[list[str]] = None,
    ):
        if invalidated_properties is None:
            invalidated_properties = list()

        parameters = GLib.Variant.new_tuple(
            GLib.Variant("s", interface_name),
            GLib.Variant("a{sv}", changed_properties),
            GLib.Variant("as", invalidated_properties),
        )
        self.connection.emit_signal(
            None,
            self.dbus_path,
            "org.freedesktop.DBus.Properties",
            "PropertiesChanged",
            parameters,
        )

    def check_idle(self) -> bool:
        """Return whether this object is idle, i.e. not currently
        handling any method calls."""
        return self.num_ongoing_calls == 0

    def _handle_method_call_async(self, *args, **kwargs) -> None:
        thread = Thread(
            target=self._handle_method_call, args=args, kwargs=kwargs, daemon=True
        )
        thread.start()

    def _handle_method_call(
        self,
        connection: Gio.DBusConnection,
        sender: str,
        object_path: str,
        interface_name: str,
        method_name: str,
        parameters: GLib.Variant,
        invocation: Gio.DBusMethodInvocation,
    ) -> None:
        full_method_name = self.__class__.__name__ + "." + method_name

        # We don't log the parameters here to avoid logging secrets
        logger.debug(f"Handling method call {full_method_name}")

        try:
            with self._avoid_exit_on_idle():
                self._handle_method_call_with_profiling_support(
                    connection,
                    sender,
                    object_path,
                    interface_name,
                    method_name,
                    parameters,
                    invocation,
                )
        finally:
            logger.debug(f"Done handling method call {full_method_name}")

    def _handle_method_call_with_profiling_support(
        self,
        connection: Gio.DBusConnection,
        sender: str,
        object_path: str,
        interface_name: str,
        method_name: str,
        parameters: GLib.Variant,
        invocation: Gio.DBusMethodInvocation,
    ) -> None:
        full_method_name = self.__class__.__name__ + "." + method_name

        if PROFILING:
            uptime = Path("/proc/uptime").read_text().split()[0]
            with tempfile.NamedTemporaryFile(
                mode="w+",
                prefix=f"{uptime}-{full_method_name}.",
                dir=PROFILES_DIR,
                delete=False,
            ) as profile_file:
                logger.info(f"Creating profile in {profile_file.name}")
                prof = cProfile.Profile()
                prof.runctx(
                    "self.handle_method_call_inner("
                    "connection, sender, object_path, interface_name,"
                    "method_name, parameters, invocation)",
                    globals=globals(),
                    locals=locals(),
                )
                stats = (
                    pstats.Stats(prof, stream=profile_file)
                    .strip_dirs()
                    .sort_stats(pstats.SortKey.CUMULATIVE)
                )
                stats.print_stats()
            return

        self._handle_method_call_inner(
            connection,
            sender,
            object_path,
            interface_name,
            method_name,
            parameters,
            invocation,
        )

    def _handle_method_call_inner(
        self,
        connection: Gio.DBusConnection,
        sender: str,
        object_path: str,
        interface_name: str,
        method_name: str,
        parameters: GLib.Variant,
        invocation: Gio.DBusMethodInvocation,
    ) -> None:
        """Here we actually figure out the correct handler function to call,
        call it, and return the result via D-Bus.

        Implements Gio.DBusInterfaceMethodCallFunc"""

        method_info: Gio.DBusMethodInfo = self._node_info.lookup_interface(
            interface_name
        ).lookup_method(method_name)

        try:
            # If a special method call handler function exists, we pass
            # it the invocation object and let it handle returning the
            # result to the caller itself.
            # This is useful for methods that need to execute code after
            # returning the result to the caller.
            try:
                handler = getattr(self, method_name + "_method_call_handler")
                handler(connection, parameters, invocation)
                return
            except AttributeError:
                # The method does not have a special handler function,
                # so we handle it here.
                pass

            # Get the method of this object that corresponds to the
            # name of the D-Bus method that was called.
            func = getattr(self, method_name)

            # Call the method with the parameters that were passed to the
            # D-Bus method call.
            result = func(*parameters)

            if not method_info.out_args:
                # The D-Bus method has no return value
                invocation.return_value(None)
                return

            if len(method_info.out_args) == 1:
                # D-Bus return values are always tuples, even if there is
                # only one return value.
                result = (result,)

            # Finish the D-Bus method call by returning the result to the
            # caller.
            return_signature = "(%s)" % "".join(
                arg.signature for arg in method_info.out_args
            )
            invocation.return_value(GLib.Variant(return_signature, result))
        except DBusError as e:
            logger.exception(e)
            invocation.return_dbus_error(e.name, str(e))
        except subprocess.CalledProcessError as e:
            logger.exception(e)
            error_name = inspect.getmodule(e).__name__ + "." + type(e).__name__
            msg = str(e)
            if e.stderr:
                stderr = GLib.markup_escape_text(e.stderr.strip())
                msg += f" Command output:\n\n<tt>{stderr}</tt>"
            invocation.return_dbus_error(error_name, msg)
        except Exception as e:
            logger.exception(e)
            module = inspect.getmodule(e)
            if module:
                error_name = module.__name__ + "." + type(e).__name__
            else:
                error_name = type(e).__name__
            if e.__class__.__module__ in ("__builtin__", "builtins"):
                error_name = "python." + error_name
            if not Gio.dbus_is_name(error_name):
                logger.warning(
                    f'Can\'t use "{error_name}" as a D-Bus error name, using "python.UnknownError" instead'
                )
                error_name = "python.UnknownError"
            invocation.return_dbus_error(error_name, str(e))

    def _handle_get_property(
        self,
        connection: Gio.DBusConnection,
        sender: str,
        object_path: str,
        interface_name: str,
        property_name: str,
    ) -> GLib.Variant:
        """Implements Gio.DBusInterfaceGetPropertyFunc"""
        logger.debug("Handling property read of %s.%s", object_path, property_name)

        with self._avoid_exit_on_idle():
            interface_info = self._node_info.lookup_interface(interface_name)
            property_info = interface_info.lookup_property(property_name)

            # Get the value of the property of this object that corresponds
            # to the name of the D-Bus property that was read.
            value = getattr(self, property_name)

            logger.debug(
                "Converting value %r to Variant type %r", value, property_info.signature
            )
            return GLib.Variant(property_info.signature, value)

    def _handle_set_property(
        self,
        connection: Gio.DBusConnection,
        sender: str,
        object_path: str,
        interface_name: str,
        property_name: str,
        value: GLib.Variant,
    ) -> bool:
        """Implements Gio.DBusInterfaceSetPropertyFunc"""
        logger.debug("Handling property write of %s.%s", object_path, property_name)

        with self._avoid_exit_on_idle():
            setattr(self, property_name, value.unpack())
            self.emit_properties_changed_signal(
                interface_name=interface_name,
                changed_properties={property_name: value},
            )
            return True

    @contextmanager
    def _avoid_exit_on_idle(self):
        """A context manager to avoid exiting on idle while handling a method call."""

        # Inform the ExitOnIdleService that we're not idle
        if self.exit_on_idle_service:
            logger.debug("Resetting idle timer")
            self.exit_on_idle_service.reset_idle_timer()

        # Keep track of the number of ongoing calls to avoid that the
        # ExitOnIdleService exits while we're still handling calls
        with self._num_ongoing_calls_lock:
            self.num_ongoing_calls += 1

        try:
            yield
        finally:
            with self._num_ongoing_calls_lock:
                self.num_ongoing_calls -= 1
