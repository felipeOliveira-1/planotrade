from typing import Union
from pydantic import BaseModel, ValidationError, validator, Field

def calculate_position_size(
    risk_amount: float, 
    entry_price: float,
    stop_price: float, 
    leverage: float
) -> float:
    """Calcula o tamanho da posição considerando risco e alavancagem"""
    risk_per_unit = abs(entry_price - stop_price)
    if risk_per_unit <= 0:
        raise ValueError("Preço de entrada e stop-loss não podem ser iguais")
    return (risk_amount / risk_per_unit) * leverage

def calculate_pnl(
    entry: float,
    exit_price: float,
    position_size: float,
    trade_type: str
) -> float:
    """Calcula lucro/prejuízo de uma operação"""
    if trade_type not in ['long', 'short']:
        raise ValueError("Tipo de operação inválido. Use 'long' ou 'short'")
        
    price_diff = exit_price - entry
    if trade_type == 'short':
        price_diff = -price_diff
        
    return price_diff * position_size

class TradeValidationSchema(BaseModel):
    entry_price: float = Field(..., gt=0)
    stop_price: float = Field(..., gt=0)
    target_price: float = Field(..., gt=0)
    leverage: float = Field(..., ge=1, le=100)
    position_size_percent: float = Field(..., ge=1, le=100)
    
    @validator('stop_price')
    def validate_stop_price(cls, v, values):
        entry = values.get('entry_price')
        if entry and v == entry:
            raise ValueError('Preço de stop não pode ser igual ao de entrada')
        return v
    
    @validator('target_price')
    def validate_target_price(cls, v, values):
        entry = values.get('entry_price')
        if entry and v == entry:
            raise ValueError('Preço alvo não pode ser igual ao de entrada')
        return v
