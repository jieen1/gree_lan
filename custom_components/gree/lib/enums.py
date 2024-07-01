import enum


@enum.unique
class Props(enum.Enum):
    POWER = "Pow"  # 开关 0为关 1为开
    NAME = "name"  # 设备名称
    HOST = "host"  # 设备ip
    FAN_SPEED = "WdSpd"  # 风速  1-12
    MODE = "Mod"  # 模式 0为普通风  2为睡眠风
    ROTATE = "Rotate"  # 是否摇头 1为摇头 0为不摇头
    LR_ANGLE = "LRAngle"  # 摇头角度  12表示60度  20表示100度 72表示360度
    TMR_ON = "TmrOn"  # 是否开启定时 1为开启 0为关闭
    TMR_ACTION = "TmrAction"  # 关机为0  1为开机
    TMR_HOUR = "TmrHour"  # 定时小时数
    TMR_MIN = "TmrMin"  # 定时分钟数

    ESTATE = "estate"  # 喜好执行状态
    J_FERR = "JFerr"


@enum.unique
class FanMode(enum.IntEnum):
    Normal = 0
    Sleep = 2


@enum.unique
class Rotate(enum.IntEnum):
    Normal = 0
    Rotate = 1


@enum.unique
class LRRotateAngle(enum.IntEnum):
    Normal = 0
    Rotate60 = 12
    Rotate100 = 20
    Rotate360 = 72


@enum.unique
class FanSpeed(enum.IntEnum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Eleven = 11
    Twelve = 12
