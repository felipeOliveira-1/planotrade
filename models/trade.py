from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class TradeType(Enum):
    LONG = 'long'
    SHORT = 'short'

@dataclass
class TradeResult:
    type: TradeType
    entry: float
    target: float
    stop: float
    result: float
    balance_before: float
    balance_after: float
    timestamp: str
    leverage: int
    position_size_percent: float

    @property
    def gain(self):
        from utils.math_utils import calculate_pnl
        return calculate_pnl(
            entry=self.entry,
            exit_price=self.target,
            position_size=(self.position_size_percent / 100) * self.leverage,
            trade_type=self.type.value
        )

    @property
    def loss(self):
        from utils.math_utils import calculate_pnl
        return calculate_pnl(
            entry=self.entry,
            exit_price=self.stop,
            position_size=(self.position_size_percent / 100) * self.leverage,
            trade_type=self.type.value
        )

    @property
    def risk_reward(self):
        return abs(self.gain / self.loss)

class AccountOperationType(Enum):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'

@dataclass
class AccountOperation:
    type: AccountOperationType
    amount: float
    timestamp: str