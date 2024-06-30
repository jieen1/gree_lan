from .features import BaseFeature, ModeFeature, TMRFeature, FanRotateFeature
from .gree_device import GreeDeviceInfo

DEVICE_MAP = {
    '828211': {
        "class": GreeDeviceInfo,
        "type_name": "FLZ-09X67Bg",
        "support_features": [BaseFeature(), ModeFeature(), TMRFeature(), FanRotateFeature()]
    }
}
