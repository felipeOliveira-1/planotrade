from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import validator

class TradeType(Enum):
    LONG = 'long'
    SHORT = 'short'

class TradeStatus(Enum):
    OPEN = 'open'
    CLOSED = 'closed'

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
    id: Optional[int] = None
    status: TradeStatus = TradeStatus.OPEN
    close_price: float = 0.0
    close_timestamp: str = None

    @validator('stop')
    def validate_stop_price(cls, v, values):
        """Valida o preço de stop"""
        if v <= 0:
            raise ValueError('Preço inválido para operação')
            
        # Validação específica para operações short
        if 'type' in values and values['type'] == TradeType.SHORT:
            if 'entry' in values and v >= values['entry']:
                raise ValueError('Para operações short, o stop deve ser menor que a entrada')
        # Validação para operações long
        elif 'type' in values and values['type'] == TradeType.LONG:
            if 'entry' in values and v <= values['entry']:
                raise ValueError('Para operações long, o stop deve ser maior que a entrada')
                
        return v

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