from .features import BaseFeature, ModeFeature, FanRotateFeature, FanRotateWithAngleFeature
from .gree_device import GreeDeviceInfo

DEVICE_MAP = {
    '828211': {
        "class": GreeDeviceInfo,
        "type_name": "FLZ-09X67Bg",
        "support_features": [BaseFeature(), ModeFeature(), FanRotateWithAngleFeature()]
    },
    '828200': {
        "class": GreeDeviceInfo,
        "type_name": "_828200",
        "support_features": [BaseFeature(), ModeFeature()]
    },
    '828202': {
        "class": GreeDeviceInfo,
        "type_name": "FL-09T65Bh",
        "support_features": [BaseFeature(), ModeFeature()]
        # Wet  MidType NOT SUPPORT
    },
    '828203': {
        "class": GreeDeviceInfo,
        "type_name": "KS-0705D",
        "support_features": [BaseFeature(), ModeFeature()]
    },
    '828204': {
        "class": GreeDeviceInfo,
        "type_name": "FSZ-3013Bg7",
        "support_features": [BaseFeature(), ModeFeature(), FanRotateFeature()]
        # Cycle NOT SUPPORT
    },
    '828205': {
        "class": GreeDeviceInfo,
        "type_name": "KS-1501RD",
        "support_features": [BaseFeature(), ModeFeature()]
        # HotWind NOT SUPPORT
    },
    '828208': {
        "class": GreeDeviceInfo,
        "type_name": "FWZ-1201Bg",
        "support_features": [BaseFeature(), ModeFeature(), FanRotateWithAngleFeature()]
        # SwUpDn  PM25 NOT SUPPORT
    },
    '828209': {
        "class": GreeDeviceInfo,
        "type_name": "FSZ-20X60Bag3",
        "support_features": [BaseFeature(), ModeFeature(), FanRotateWithAngleFeature()]
        # Cycle  SwUpDn UpDnAngle NOT SUPPORT
    },
    '828210': {
        "class": GreeDeviceInfo,
        "type_name": "_828210",
        "support_features": [BaseFeature(), ModeFeature(), FanRotateWithAngleFeature()]
        # HotWind  HotwindOnOff NOT SUPPORT
    },
    '828212': {
        "class": GreeDeviceInfo,
        "type_name": "_828212",
        "support_features": [BaseFeature(), ModeFeature(), FanRotateFeature()]
    }
}
