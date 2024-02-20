# SPDX-FileCopyrightText: © 2024 Adrian Dombeck <adrian.dombeck@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import abstractmethod

from gi.repository import Gio, GLib


class DBusError(Exception):
    """An exception that can be returned as an error by a D-Bus method"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @classmethod
    def is_instance(cls, err) -> bool:
        if not Gio.DBusError.is_remote_error(err):
            return False

        return Gio.DBusError.get_remote_error(err) == cls.name

    @classmethod
    def strip_remote_error(cls, err: GLib.Error):
        """This method is meant for clients which handle a DBusError
        and want to remove the D-Bus error prefix from the message.

        This is a workaround for Gio.DBusError.strip_remote_error being
        broken in pygobject, see
        https://gitlab.gnome.org/GNOME/pygobject/-/issues/342"""

        prefix = f"GDBus.Error:{cls.name}: "
        if err.message.startswith(prefix):
            err.message = err.message[len(prefix) :]
            return

        prefix = "GDBus.Error:"
        if err.message.startswith(prefix):
            err.message = err.message[len(prefix) :]
