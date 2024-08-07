import asyncio
import logging
import re

from custom_components.gree.lib import network
from custom_components.gree.lib.enums import Props
from custom_components.gree.lib.exceptions import DeviceNotBoundError, DeviceTimeoutError
from custom_components.gree.lib.gree_device import GreeDeviceInfo

"""
COPY FROM https://github.com/cmroche/greeclimate/blob/master/greeclimate/device.py

UPDATE BY jieen1
"""


class Device:

    def __init__(self, device_info: GreeDeviceInfo):
        self._logger = logging.getLogger(__name__)

        self.device_info = device_info
        self.device_key = None

        """ Device properties """
        self.hid = None
        self.version = None
        self._properties = None
        self._dirty = []

    async def bind(self, key=None):
        """Run the binding procedure.

        Binding is a finnicky procedure, and happens in 1 of 2 ways:
            1 - Without the key, binding must pass the device info structure immediately following
                the search devices procedure. There is only a small window to complete registration.
            2 - With a key, binding is implicit and no further action is required

            Both approaches result in a device_key which is used as like a persitent session id.

        Args:
            key (str): The device key, when provided binding is a NOOP, if None binding will
                       attempt to negatiate the key with the device.

        Raises:
            DeviceNotBoundError: If binding was unsuccessful and no key returned
            DeviceTimeoutError: The device didn't respond
        """

        if not self.device_info:
            raise DeviceNotBoundError

        self._logger.info("Starting device binding to %s", str(self.device_info))

        try:
            if key:
                self.device_key = key
            else:
                self.device_key = await network.bind_device(
                    self.device_info, announce=False
                )
        except asyncio.TimeoutError:
            raise DeviceTimeoutError

        if not self.device_key:
            raise DeviceNotBoundError
        else:
            self._logger.info("Bound to device using key %s", self.device_key)

    async def request_version(self) -> None:
        """Request the firmware version from the device."""
        ret = await network.request_state(["hid"], self.device_info, self.device_key)
        self.hid = ret.get("hid")

        # Ex: hid = 362001000762+U-CS532AE(LT)V3.31.bin
        if self.hid:
            match = re.search(r"(?<=V)([\d.]+)\.bin$", self.hid)
            self.version = match and match.group(1)

    async def update_state(self):
        """Update the internal state of the device structure of the physical device"""
        if not self.device_key:
            await self.bind()

        self._logger.debug("Updating device properties for (%s)", str(self.device_info))

        props = self.device_info.d_pros

        try:
            self._properties = await network.request_state(
                props, self.device_info, self.device_key
            )

            # This check should prevent need to do version & device overrides
            # to correctly compute the temperature. Though will need to confirm
            # that it resolves all possible cases.
            if not self.hid:
                await self.request_version()

        except asyncio.TimeoutError:
            raise DeviceTimeoutError

    async def push_state_update(self):
        """Push any pending state updates to the unit"""
        if not self._dirty:
            return

        if not self.device_key:
            await self.bind()

        self._logger.debug("Pushing state updates to (%s)", str(self.device_info))

        props = {}
        for name in self._dirty:
            value = self._properties.get(name)
            self._logger.debug("Sending remote state update %s -> %s", name, value)
            props[name] = value

        self._dirty.clear()

        try:
            await network.send_state(props, self.device_info, key=self.device_key)
        except asyncio.TimeoutError:
            raise DeviceTimeoutError

    def get_property(self, name):
        """Generic lookup of properties tracked from the physical device"""
        if self._properties:
            return self._properties.get(name.value)
        return None

    def set_property(self, name, value):
        """Generic setting of properties for the physical device"""
        if not self._properties:
            self._properties = {}

        if self._properties.get(name.value) == value:
            return
        else:
            self._properties[name.value] = value
            if name.value not in self._dirty:
                self._dirty.append(name.value)

    @property
    def power(self) -> bool:
        return bool(self.get_property(Props.POWER))

    @power.setter
    def power(self, value: int):
        self.set_property(Props.POWER, int(value))

    @property
    def mode(self) -> int:
        return self.get_property(Props.MODE)

    @mode.setter
    def mode(self, value: int):
        self.set_property(Props.MODE, int(value))

    @property
    def fan_speed(self) -> int:
        return self.get_property(Props.FAN_SPEED)

    @fan_speed.setter
    def fan_speed(self, value: int):
        self.set_property(Props.FAN_SPEED, int(value))

    @property
    def rotate(self) -> int:
        return self.get_property(Props.ROTATE)

    @rotate.setter
    def rotate(self, value: int):
        self.set_property(Props.ROTATE, int(value))

    @property
    def lr_angle(self) -> int:
        return self.get_property(Props.LR_ANGLE)

    @lr_angle.setter
    def lr_angle(self, value: int):
        self.set_property(Props.LR_ANGLE, int(value))
