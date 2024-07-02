import logging
import math
from typing import Any

from homeassistant.components.fan import (
    FanEntity,
    FanEntityFeature
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util.percentage import ranged_value_to_percentage, int_states_in_range, percentage_to_ranged_value

from .bridge import DeviceDataUpdateCoordinator
from .constant import DOMAIN, COORDINATORS, DISPATCHERS, DISPATCH_DEVICE_DISCOVERED
from .lib.enums import Rotate, LRRotateAngle

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Gree fan device from a config entry."""

    @callback
    def init_device(coordinator):
        """Register the device."""
        async_add_entities([GreeFanEntity(coordinator)])

    for coordinator in hass.data[DOMAIN][COORDINATORS]:
        init_device(coordinator)

    hass.data[DOMAIN][DISPATCHERS].append(
        async_dispatcher_connect(hass, DISPATCH_DEVICE_DISCOVERED, init_device)
    )


class GreeFanEntity(FanEntity, CoordinatorEntity[DeviceDataUpdateCoordinator]):
    _attr_supported_features = FanEntityFeature.SET_SPEED | FanEntityFeature.OSCILLATE

    def __init__(self, coordinator: DeviceDataUpdateCoordinator, max_step=12) -> None:
        """Initialize the Gree device."""
        super().__init__(coordinator)
        self._name = coordinator.device.device_info.name
        self._mac = coordinator.device.device_info.mac
        self._step_range: tuple[int, int] | None = (1, max_step) if max_step else None
        self._attr_speed_count = max_step

    @property
    def name(self) -> str:
        """Return the name of the device."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique id for the device."""
        return self._mac

    async def async_turn_on(self,
                            percentage: int | None = None,
                            preset_mode: str | None = None,
                            **kwargs: Any) -> None:
        """Turn on the device."""
        _LOGGER.debug("Turning on fan for device %s", self._name)

        self.coordinator.device.power = True
        await self.coordinator.push_state_update()
        self.async_write_ha_state()
        await self.async_set_percentage(percentage)

    async def async_turn_off(self) -> None:
        """Turn off the device."""
        _LOGGER.debug("Turning off HVAC for device %s", self._name)

        self.coordinator.device.power = False
        await self.coordinator.push_state_update()
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.device.power == 1

    @property
    def percentage(self) -> int | None:
        """Return the current speed as a percentage."""
        speed = self.coordinator.device.fan_speed
        if speed is None:
            return None

        if self._step_range:
            return ranged_value_to_percentage(
                self._step_range, speed
            )
        return speed

    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        if self._step_range is None:
            return super().speed_count
        return int_states_in_range(self._step_range)

    async def async_set_percentage(self, percentage: int) -> None:
        if percentage is None:
            return
        speed = percentage
        if self._step_range:
            speed = math.ceil(percentage_to_ranged_value(self._step_range, percentage))
        self.coordinator.device.fan_speed = speed
        await self.coordinator.push_state_update()
        self.async_write_ha_state()

    @property
    def oscillating(self) -> bool | None:
        return self.coordinator.device.rotate == Rotate.Rotate.value

    async def async_oscillate(self, oscillating: bool) -> None:
        if oscillating is None:
            return
        self.coordinator.device.rotate = Rotate.Rotate.value if oscillating else Rotate.Normal.value
        self.coordinator.device.lr_angle = LRRotateAngle.Rotate60.value
        await self.coordinator.push_state_update()
        self.async_write_ha_state()
