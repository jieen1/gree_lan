from abc import ABC
from typing import List

from .enums import Props


class Feature(ABC):
    support_pros: List[Props] = []

    def __init__(self, support_pros) -> None:
        self.support_pros = support_pros


class BaseFeature(Feature):
    SUPPORT_PROPS = [Props.POWER, Props.FAN_SPEED, Props.NAME, Props.HOST]

    def __init__(self) -> None:
        super().__init__(self.SUPPORT_PROPS)


class ModeFeature(Feature):
    SUPPORT_PROPS = [Props.MODE]

    def __init__(self) -> None:
        super().__init__(self.SUPPORT_PROPS)


class FanRotateFeature(Feature):
    SUPPORT_PROPS = [Props.ROTATE, Props.LR_ANGLE]

    def __init__(self) -> None:
        super().__init__(self.SUPPORT_PROPS)


class TMRFeature(Feature):
    SUPPORT_PROPS = [Props.TMR_ON, Props.TMR_ACTION, Props.TMR_HOUR, Props.TMR_MIN]

    def __init__(self) -> None:
        super().__init__(self.SUPPORT_PROPS)
