from abc import ABC
from typing import List

from .enums import Props


class Feature(ABC):
    support_pros: List[Props] = []

    def __init__(self, support_pros) -> None:
        self.support_pros = support_pros

    def rotate(self) -> bool:
        return False

    def mode(self) -> bool:
        return False

    def lr_angle(self) -> bool:
        return False


class BaseFeature(Feature):
    SUPPORT_PROPS = [Props.POWER, Props.FAN_SPEED, Props.NAME, Props.HOST]

    def __init__(self) -> None:
        super().__init__(self.SUPPORT_PROPS)


class ModeFeature(Feature):
    SUPPORT_PROPS = [Props.MODE]

    def __init__(self) -> None:
        super().__init__(self.SUPPORT_PROPS)

    def mode(self) -> bool:
        return True


class FanRotateFeature(Feature):
    SUPPORT_PROPS = [Props.ROTATE]

    def __init__(self) -> None:
        super().__init__(self.SUPPORT_PROPS)

    def rotate(self) -> bool:
        return True


class FanRotateWithAngleFeature(Feature):
    SUPPORT_PROPS = [Props.ROTATE, Props.LR_ANGLE]

    def __init__(self) -> None:
        super().__init__(self.SUPPORT_PROPS)

    def rotate(self) -> bool:
        return True

    def lr_angle(self) -> bool:
        return True


