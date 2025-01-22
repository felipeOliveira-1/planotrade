from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
from datetime import datetime

T = TypeVar('T')

class Repository(ABC, Generic[T]):
    """Interface base para repositórios"""
    
    @abstractmethod
    def add(self, entity: T) -> None:
        """Adiciona uma nova entidade ao repositório"""
        pass
    
    @abstractmethod
    def get(self, id: str) -> T:
        """Obtém uma entidade pelo ID"""
        pass
    
    @abstractmethod
    def list(self) -> List[T]:
        """Lista todas as entidades"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> None:
        """Atualiza uma entidade existente"""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> None:
        """Remove uma entidade pelo ID"""
        pass

class UnitOfWork(ABC):
    """Interface para Unit of Work"""
    
    @abstractmethod
    def __enter__(self):
        """Inicia uma transação"""
        pass
    
    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Finaliza a transação"""
        pass
    
    @abstractmethod
    def commit(self):
        """Confirma as alterações"""
        pass
    
    @abstractmethod
    def rollback(self):
        """Desfaz as alterações"""
        pass