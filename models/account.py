from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from .trade import TradeResult, AccountOperation

@dataclass
class TradePlan:
    initial_balance: float
    total_trades: int
    current_balance: float = field(init=False)
    completed_trades: int = 0
    trade_history: List[TradeResult] = field(default_factory=list)
    account_operations: List[AccountOperation] = field(default_factory=list)
    max_drawdown: float = 0
    max_balance: float = field(init=False)
    leverage: int = 2  # Default 2x leverage (1-10)
    position_size_percent: float = 10  # Default 10% size (1-100)
    risk_per_trade: float = 2  # Default 2% risk per trade (0-100)

    def __post_init__(self):
        self.current_balance = self.initial_balance
        self.max_balance = self.initial_balance

    def get_risk_amount(self) -> float:
        return self.current_balance * (self.position_size_percent / 100)