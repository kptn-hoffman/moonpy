from enum import Enum, auto

class State(Enum):
    BUY  = auto()
    SELL = auto()

class OrderSide(Enum):
    BUY  = auto()
    SELL = auto()

class OrderType(Enum):
    LIMIT             = auto()
    MARKET            = auto()
    STOP_LOSS         = auto()
    STOP_LOSS_LIMIT   = auto()
    TAKE_PROFIT       = auto()
    TAKE_PROFIT_LIMIT = auto()
    LIMIT_MAKER       = auto()

class WalletType(Enum):
    SPOT   = auto()
    MARGIN = auto()