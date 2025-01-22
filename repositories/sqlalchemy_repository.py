from sqlalchemy import create_engine, Column, Integer, Float, String, Enum, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime
from models.trade import TradeResult, TradeType
from core.repository import Repository, UnitOfWork
from config.settings import settings

Base = declarative_base()

class TradeModel(Base):
    """Modelo SQLAlchemy para TradeResult"""
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(TradeType), nullable=False)
    entry = Column(Float, nullable=False)
    target = Column(Float, nullable=False)
    stop = Column(Float, nullable=False)
    result = Column(Float, default=0)
    balance_before = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    leverage = Column(Integer, nullable=False)
    position_size_percent = Column(Float, nullable=False)

class SQLAlchemyRepository(Repository[TradeResult]):
    """Implementação de Repository usando SQLAlchemy"""
    
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
    def _to_model(self, entity: TradeResult) -> TradeModel:
        """Converte TradeResult para TradeModel"""
        return TradeModel(
            type=entity.type,
            entry=entity.entry,
            target=entity.target,
            stop=entity.stop,
            result=entity.result,
            balance_before=entity.balance_before,
            balance_after=entity.balance_after,
            timestamp=entity.timestamp,
            leverage=entity.leverage,
            position_size_percent=entity.position_size_percent
        )
        
    def _from_model(self, model: TradeModel) -> TradeResult:
        """Converte TradeModel para TradeResult"""
        return TradeResult(
            type=model.type,
            entry=model.entry,
            target=model.target,
            stop=model.stop,
            result=model.result,
            balance_before=model.balance_before,
            balance_after=model.balance_after,
            timestamp=model.timestamp,
            leverage=model.leverage,
            position_size_percent=model.position_size_percent
        )
        
    def add(self, entity: TradeResult) -> None:
        session = self.Session()
        try:
            session.add(self._to_model(entity))
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def get(self, id: int) -> Optional[TradeResult]:
        session = self.Session()
        try:
            model = session.query(TradeModel).get(id)
            return self._from_model(model) if model else None
        finally:
            session.close()
            
    def list(self) -> List[TradeResult]:
        session = self.Session()
        try:
            models = session.query(TradeModel).all()
            return [self._from_model(m) for m in models]
        finally:
            session.close()
            
    def update(self, entity: TradeResult) -> None:
        session = self.Session()
        try:
            model = session.query(TradeModel).get(entity.id)
            if model:
                model.type = entity.type
                model.entry = entity.entry
                model.target = entity.target
                model.stop = entity.stop
                model.result = entity.result
                model.balance_before = entity.balance_before
                model.balance_after = entity.balance_after
                model.timestamp = entity.timestamp
                model.leverage = entity.leverage
                model.position_size_percent = entity.position_size_percent
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def delete(self, id: int) -> None:
        session = self.Session()
        try:
            model = session.query(TradeModel).get(id)
            if model:
                session.delete(model)
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

class SQLAlchemyUnitOfWork(UnitOfWork):
    """Implementação de Unit of Work para SQLAlchemy"""
    
    def __init__(self, repository: SQLAlchemyRepository):
        self.repository = repository
        self.session = repository.Session()
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        self.session.close()
        
    def commit(self):
        self.session.commit()
        
    def rollback(self):
        self.session.rollback()