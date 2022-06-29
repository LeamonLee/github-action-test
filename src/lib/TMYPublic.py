from enum import Enum, auto

class DevInterface(Enum):
    UNKNOWN = -1
    LAN = 0
    COMPORT = auto()
    ALL = auto() # all interface selected

class RFMode(Enum):
    TX      = 0
    RX      = auto()

class RetCode(Enum):
    #_baseVersion = "3.3.15.0"

    OK                      = 0
    WARNING                 = auto()
    ERROR                   = auto()
    NO_RESPONSE             = auto()
    # genereal scan & init
    ERROR_GET_SN            = 10
    ERROR_DEV_TYPE          = auto()
    ERROR_SCAN              = auto()
    ERROR_INIT_OBJECT       = auto()
    ERROR_DEV_NOT_INIT      = auto()
    ERROR_METHOD_NOT_FOUND  = auto()
    ERROR_METHOD_NOT_SUPPORT= auto()
    ERROR_REFLECTION        = auto()
    ERROR_POWER             = auto()
    ERROR_EXPORT_LOG        = auto()
    # network
    ERROR_COMM_NOT_INIT  = 20
    ERROR_COMM_INIT      = auto()
    ERROR_COMM_CONNECT_TIMEOUT = auto()
    ERROR_DISCONNECT        = auto()
    ERROR_SOCKET            = auto()
    ERROR_SEND_CMD          = auto()
    ERROR_RESP_CMD          = auto()
    # device object
    ERROR_DEV_COUNT_ZERO    = 30
    # CMD to device
    ERROR_CMD               = 40
    ERROR_CMD_INIT          = auto()
    # Beamforming device
    ERROR_BF_STATE          = 100
    ERROR_BF_AAKIT          = auto()
    ERROR_BF_NO_AAKIT       = auto()
    ERROR_BF_CALI_PATH      = auto()
    ERROR_BF_BEAM           = auto()
    ERROR_BF_GAIN           = auto()
    ERROR_BF_PHASE          = auto()
    ERROR_BF_RFMODE         = auto()
    ERROR_BF_CALI_INCOMPLTE = auto()
    ERROR_BF_CALI_PARSE     = auto()
    ERROR_BF_TC             = auto()
    ERROR_BF_BEAM_FILE      = auto()
    # UD device
    ERROR_FREQ_EQUATION     = 250
    WARNING_HARMONIC        = auto()
    ERROR_HARMONIC_BLOCK    = auto()
    ERROR_PLO_UNLOCK        = 253
    ERROR_PLO_CRC           = auto()
    ERROR_UD_STATE          = auto()

class UDState(Enum):
    NO_SET          = -1
    PLO_LOCK        = 0
    CH1             = auto()
    CH2             = auto() # ignore it if single UD
    OUT_10M         = auto()
    OUT_100M        = auto()
    SOURCE_100M     = auto() # 0:Internal, 1:External
    LED_100M        = auto() # 0:OFF, 1:WHITE, 2:BLUE
    PWR_5V          = auto()
    PWR_9V          = auto()
