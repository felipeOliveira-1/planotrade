from datetime import datetime
from typing import Optional, List
from models.account import TradePlan
from models.trade import TradeResult, TradeType
from core.repository import Repository, UnitOfWork
from utils.math_utils import calculate_position_size, calculate_pnl

class TradeService:
    """Serviço para gerenciamento de operações de trade"""
    
    def __init__(self, 
                 trade_plan: TradePlan,
                 trade_repository: Repository[TradeResult],
                 unit_of_work: UnitOfWork):
        self.trade_plan = trade_plan
        self.trade_repository = trade_repository
        self.unit_of_work = unit_of_work

    def calculate_position(self, entry: float, stop: float) -> float:
        """Calcula o tamanho da posição"""
        risk_amount = self.trade_plan.get_risk_amount()
        return calculate_position_size(
            risk_amount=risk_amount,
            entry_price=entry,
            stop_price=stop,
            leverage=self.trade_plan.leverage
        )

    def add_trade_result(self, trade_result: TradeResult) -> None:
        """Adiciona um novo resultado de trade"""
        with self.unit_of_work:
            self.trade_repository.add(trade_result)
            self.trade_plan.trade_history.append(trade_result)
            self.trade_plan.current_balance += trade_result.result
            self.trade_plan.completed_trades += 1

    def get_remaining_trades(self) -> int:
        """Retorna o número de trades restantes"""
        return self.trade_plan.total_trades - self.trade_plan.completed_trades

    def get_open_trades(self) -> List[TradeResult]:
        """Retorna uma lista de trades abertos"""
        return [t for t in self.trade_repository.list() if t.result == 0]

    def create_trade(self, trade_data: dict) -> TradeResult:
        """Cria um novo trade"""
        with self.unit_of_work:
            # Validação e criação do trade
            trade = self._validate_and_create_trade(trade_data)
            
            # Adiciona ao repositório
            self.trade_repository.add(trade)
            
            return trade

    def _validate_and_create_trade(self, trade_data: dict) -> TradeResult:
        """Valida os dados e cria um novo TradeResult"""
        from core.schemas import TradeSchema
        
        # Valida os dados usando o schema
        validated_data = TradeSchema(**trade_data).dict()
        
        # Cria o trade
        return TradeResult(
            type=TradeType(validated_data['type']),
            entry=validated_data['entry'],
            target=validated_data['target'],
            stop=validated_data['stop'],
            result=0,
            balance_before=self.trade_plan.current_balance,
            balance_after=self.trade_plan.current_balance,
            timestamp=validated_data['timestamp'],
            leverage=validated_data['leverage'],
            position_size_percent=validated_data['position_size']
        )

    # ... (outros métodos atualizados)
