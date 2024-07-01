"""Support for interface with a Gree climate systems."""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .bridge import DeviceDataUpdateCoordinator
from .constant import COORDINATORS, DISPATCH_DEVICE_DISCOVERED, DISPATCHERS, DOMAIN


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Gree HVAC device from a config entry."""

    @callback
    def init_device(coordinator):
        """Register the device."""
        async_add_entities(
            [
                GreeTowerFanModeEntity(coordinator),
            ]
        )

    for coordinator in hass.data[DOMAIN][COORDINATORS]:
        init_device(coordinator)

    hass.data[DOMAIN][DISPATCHERS].append(
        async_dispatcher_connect(hass, DISPATCH_DEVICE_DISCOVERED, init_device)
    )


class GreeTowerFanModeEntity(CoordinatorEntity[DeviceDataUpdateCoordinator], SwitchEntity):
    """Representation of the front panel light on the device."""

    def __init__(self, coordinator):
        """Initialize the Gree device."""
        super().__init__(coordinator, "fan mode")

    @property
    def device_class(self):
        """Return the class of this device, from component DEVICE_CLASSES."""
        return SwitchDeviceClass.SWITCH

    @property
    def is_on(self) -> bool:
        """Return if the light is turned on."""
        return self.coordinator.device.mode == 1

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        self.coordinator.device.mode = 1
        await self.coordinator.push_state_update()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        self.coordinator.device.mode = 0
        await self.coordinator.push_state_update()
        self.async_write_ha_state()
