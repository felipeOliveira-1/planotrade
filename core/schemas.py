from pydantic import BaseModel, validator, Field
from typing import Literal
from datetime import datetime

class TradeSchema(BaseModel):
    """Schema para validação de dados de trade"""
    type: Literal['long', 'short']
    leverage: int = Field(ge=1, le=10)
    position_size: float = Field(ge=1, le=100)
    entry: float
    target: float
    stop: float
    timestamp: datetime = Field(default_factory=datetime.now)

    @validator('target', 'stop')
    def validate_prices(cls, value, values):
        if 'type' not in values:
            return value
            
        if values['type'] == 'long':
            if 'entry' in values:
                if value <= values['entry']:
                    raise ValueError('Preço inválido para operação long')
        else:
            if 'entry' in values:
                if value >= values['entry']:
                    raise ValueError('Preço inválido para operação short')
        return value

    @validator('position_size')
    def validate_position_size(cls, value):
        if not 1 <= value <= 100:
            raise ValueError('Tamanho da posição deve estar entre 1% e 100%')
        return value

class TradePlanSchema(BaseModel):
    """Schema para validação de TradePlan"""
    initial_balance: float = Field(gt=0)
    risk_per_trade: float = Field(ge=0.1, le=5)
    total_trades: int = Field(ge=1)
    leverage: int = Field(ge=1, le=10)