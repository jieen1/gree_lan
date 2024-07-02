from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .bridge import DeviceDataUpdateCoordinator
from .constant import COORDINATORS, DISPATCH_DEVICE_DISCOVERED, DISPATCHERS, DOMAIN
from .lib.enums import LRRotateAngle

LRAngleDescMap = {
    LRRotateAngle.Normal: "已关闭",
    LRRotateAngle.Rotate60: "60°",
    LRRotateAngle.Rotate100: "100°",
    LRRotateAngle.Rotate360: "360°",
}

LRAngleDescReserveMap = {desc: angle for (angle, desc) in LRAngleDescMap.items()}


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Gree fan rotate mode from a config entry."""

    @callback
    def init_device(coordinator):
        """Register the device."""
        async_add_entities(
            [
                GreeTowerFanRotateAngleEntity(coordinator),
            ]
        )

    for coordinator in hass.data[DOMAIN][COORDINATORS]:
        init_device(coordinator)

    hass.data[DOMAIN][DISPATCHERS].append(
        async_dispatcher_connect(hass, DISPATCH_DEVICE_DISCOVERED, init_device)
    )


class GreeTowerFanRotateAngleEntity(CoordinatorEntity[DeviceDataUpdateCoordinator], SelectEntity):
    """Representation of the front panel light on the device."""

    def __init__(self, coordinator):
        """Initialize the Gree device."""
        super().__init__(coordinator)
        self._desc = "Rotate Angle"
        self._name = f"{coordinator.device.device_info.name}"
        self._mac = coordinator.device.device_info.mac

    @property
    def name(self):
        """Return the name of the node."""
        return f"{self._name} {self._desc}"

    @property
    def unique_id(self):
        """Return the unique id based for the node."""
        return f"{self._mac}_{self._desc}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return info about the device."""
        return DeviceInfo(
            connections={(CONNECTION_NETWORK_MAC, self._mac)},
            identifiers={(DOMAIN, self._mac)},
            manufacturer="Gree",
            name=self._name,
        )

    @property
    def options(self) -> list[str]:
        return list(LRAngleDescMap.values())

    @property
    def current_option(self) -> str | None:
        return LRAngleDescMap.get(LRRotateAngle(self.coordinator.device.lr_angle))

    async def async_select_option(self, option: str) -> None:
        if option and LRAngleDescReserveMap.get(option):
            value: int = LRAngleDescReserveMap.get(option).value
            rotate_value = 1 if value != 0 else 0
            self.coordinator.device.rotate = rotate_value
            self.coordinator.device.lr_angle = value
            await self.coordinator.push_state_update()
            self.async_write_ha_state()
