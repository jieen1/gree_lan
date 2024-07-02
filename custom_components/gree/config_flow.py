"""Config flow for Gree."""
from typing import Any

from homeassistant.components.network import async_get_ipv4_broadcast_addresses
from homeassistant.config_entries import ConfigFlow
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_entry_flow

from .constant import DISCOVERY_TIMEOUT, DOMAIN
from .lib.discovery import Discovery


async def _async_has_devices(hass: HomeAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    gree_discovery = Discovery(DISCOVERY_TIMEOUT)
    bcast_addr = list(await async_get_ipv4_broadcast_addresses(hass))
    devices = await gree_discovery.scan(
        wait_for=DISCOVERY_TIMEOUT, bcast_ifaces=bcast_addr
    )
    return len(devices) > 0


class GreeLanFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a AdGuard Home config flow."""

    async def _show_setup_form(
            self, errors: dict[str, str] | None = None
    ) -> FlowResult:
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            errors=errors or {},
        )

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initiated by the user."""
        return await self._show_setup_form(user_input)


config_entry_flow.register_discovery_flow(DOMAIN, "Gree Fan", _async_has_devices)
