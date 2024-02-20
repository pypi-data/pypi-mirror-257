#!/usr/bin/env python3
import logging
import time

from gi.repository import Gio
from gdbus_util import DBusObject, ExitOnIdleService


DBUS_NAME = "org.example.Hello"
TIMEOUT = 30


class HelloService(DBusObject, ExitOnIdleService):
    dbus_info = """
        <node>
            <interface name='org.example.Hello'>                
                <method name='SayHello'>
                    <arg name='name' direction='in' type='s'/>
                    <arg name='output' direction='out' type='s'/>
                </method>
                <method name='Sleep'>
                    <arg name='seconds' direction='in' type='u'/>                    
                </method>                
            </interface>
        </node>
        """

    dbus_path = "/org/example/Hello"

    def SayHello(self, name: str):
        return f"Hello, {name}!"

    def Sleep(self, seconds: int):
        time.sleep(seconds)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bus = Gio.bus_get_sync(Gio.BusType.SESSION)
service = HelloService(connection=bus, name=DBUS_NAME, timeout=TIMEOUT)
service.run()
