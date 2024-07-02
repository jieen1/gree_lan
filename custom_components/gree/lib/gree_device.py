from typing import List, final

from .features import Feature


class GreeDevice:
    d_type: str
    d_name: str
    d_type_id: str
    d_features: None | List[Feature]

    def __init__(self, d_type, name, type_id, features=None) -> None:
        self.d_type = d_type
        self.d_name = name
        self.d_type_id = type_id
        self.d_features = features

    @final
    def support_features(self) -> List[Feature]:
        if self.d_features is None:
            return []
        return self.d_features


class DeviceInfo:
    """Device information class, used to identify and connect

    Attributes
        ip: IP address (ipv4 only) of the physical device
        port: Usually this will always be 7000
        mac: mac address, in the format 'aabbcc112233'
        name: Name of unit, if available
        mid: device type id
    """

    def __init__(self, ip, port, mac, name, mid, brand=None, model=None, version=None):
        self.ip = ip
        self.port = port
        self.mac = mac
        self.name = name if name else mac.replace(":", "")
        self.brand = brand
        self.model = model
        self.version = version
        self.mid = mid

    def __str__(self):
        return f"Device: {self.mid} {self.name} @ {self.ip}:{self.port} (mac: {self.mac})"

    def __eq__(self, other):
        """Check equality based on Device Info properties"""
        if isinstance(other, DeviceInfo):
            return (
                    self.mac == other.mac
                    and self.name == other.name
                    and self.brand == other.brand
                    and self.model == other.model
                    and self.version == other.version
                    and self.mid == other.mid
            )
        return False

    def __ne__(self, other):
        """Check inequality based on Device Info properties"""
        return not self.__eq__(other)


class GreeDeviceInfo(GreeDevice, DeviceInfo):
    d_pros: list = []

    def __init__(self, type_name, name, type_id, ip, port, mac, brand=None, model=None, version=None,
                 feature=None) -> None:
        GreeDevice.__init__(self, type_name, name, type_id, feature)
        DeviceInfo.__init__(self, ip, port, mac, name, type_id, brand, model, version)
        if feature:
            props_set = set()
            for feature in self.support_features():
                for prop in feature.support_pros:
                    props_set.add(prop)
            self.d_pros = list(props_set)
