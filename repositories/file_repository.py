import json
from pathlib import Path
from typing import Type, List, Optional
from datetime import datetime
from core.repository import Repository, UnitOfWork
from models.trade import TradeResult
from models.account import TradePlan

class FileRepository(Repository[TradeResult]):
    """Implementação de Repository para persistência em arquivos JSON"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._ensure_file_exists()
        
    def _ensure_file_exists(self) -> None:
        """Cria o arquivo se não existir"""
        if not self.file_path.exists():
            self.file_path.write_text('[]')
            
    def _load_data(self) -> List[dict]:
        """Carrega os dados do arquivo"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Converte IDs para int se necessário
            for item in data:
                if 'id' in item and isinstance(item['id'], str):
                    item['id'] = int(item['id'])
            return data
            
    def _save_data(self, data: List[dict]) -> None:
        """Salva os dados no arquivo"""
        # Converte IDs para int se necessário
        for item in data:
            if 'id' in item and isinstance(item['id'], str):
                item['id'] = int(item['id'])
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, default=str)
            
    def add(self, entity: TradeResult) -> None:
        data = self._load_data()
        # Gera um ID sequencial se não existir
        if entity.id is None:
            entity.id = max([item.get('id', 0) for item in data], default=0) + 1
        data.append(entity.__dict__)
        self._save_data(data)
        
    def get(self, id: int) -> Optional[TradeResult]:
        data = self._load_data()
        for item in data:
            if item.get('id') == id:
                # Converte strings para int se necessário
                if isinstance(item.get('id'), str):
                    item['id'] = int(item['id'])
                return TradeResult(**item)
        return None
        
    def list(self) -> List[TradeResult]:
        data = self._load_data()
        # Converte IDs para int se necessário
        for item in data:
            if 'id' in item and isinstance(item['id'], str):
                item['id'] = int(item['id'])
        return [TradeResult(**item) for item in data]
        
    def update(self, entity: TradeResult) -> None:
        data = self._load_data()
        for i, item in enumerate(data):
            # Converte strings para int se necessário
            item_id = int(item.get('id')) if isinstance(item.get('id'), str) else item.get('id')
            if item_id == entity.id:
                data[i] = entity.__dict__
                break
        self._save_data(data)
        
    def delete(self, id: str) -> None:
        data = self._load_data()
        data = [item for item in data if item.get('id') != id]
        self._save_data(data)
        
    def load_trade_plan(self) -> TradePlan:
        """Carrega o TradePlan do arquivo"""
        data = self._load_data()
        if not data:
            return TradePlan(initial_balance=1000.0, total_trades=10)
            
        trade_plan = TradePlan(
            initial_balance=data.get('current_balance', 1000.0),
            total_trades=10
        )
        
        # Carrega histórico de trades
        trade_plan.trade_history = [
            TradeResult(**trade_data) for trade_data in data.get('trade_history', [])
        ]
        
        return trade_plan
        
    def save_trade_plan(self, trade_plan: TradePlan) -> None:
        """Salva o TradePlan no arquivo"""
        data = {
            'current_balance': trade_plan.current_balance,
            'completed_trades': trade_plan.completed_trades,
            'max_drawdown': trade_plan.max_drawdown,
            'max_balance': trade_plan.max_balance,
            'leverage': trade_plan.leverage,
            'position_size_percent': trade_plan.position_size_percent,
            'trade_history': [trade.__dict__ for trade in trade_plan.trade_history],
            'account_operations': trade_plan.account_operations
        }
        self._save_data(data)

class FileUnitOfWork(UnitOfWork):
    """Implementação de Unit of Work para operações com arquivos"""
    
    def __init__(self, repository: FileRepository):
        self.repository = repository
        self._original_data = None
        
    def __enter__(self):
        self._original_data = self.repository._load_data()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
            
    def commit(self):
        self._original_data = None
        
    def rollback(self):
        if self._original_data is not None:
            self.repository._save_data(self._original_data)