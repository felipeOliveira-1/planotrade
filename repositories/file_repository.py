import json
from pathlib import Path
from typing import Type, List, Optional
from datetime import datetime
from core.repository import Repository, UnitOfWork
from models.trade import TradeResult

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
            return json.load(f)
            
    def _save_data(self, data: List[dict]) -> None:
        """Salva os dados no arquivo"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, default=str)
            
    def add(self, entity: TradeResult) -> None:
        data = self._load_data()
        data.append(entity.__dict__)
        self._save_data(data)
        
    def get(self, id: str) -> Optional[TradeResult]:
        data = self._load_data()
        for item in data:
            if item.get('id') == id:
                return TradeResult(**item)
        return None
        
    def list(self) -> List[TradeResult]:
        data = self._load_data()
        return [TradeResult(**item) for item in data]
        
    def update(self, entity: TradeResult) -> None:
        data = self._load_data()
        for i, item in enumerate(data):
            if item.get('id') == entity.id:
                data[i] = entity.__dict__
                break
        self._save_data(data)
        
    def delete(self, id: str) -> None:
        data = self._load_data()
        data = [item for item in data if item.get('id') != id]
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