from repositories.file_repository import FileRepository, FileUnitOfWork
from repositories.sqlalchemy_repository import SQLAlchemyRepository, SQLAlchemyUnitOfWork
from services.trade_service import TradeService
from models.account import TradePlan
from config.settings import settings

class ServiceFactory:
    """Factory para criação dos serviços e dependências"""
    
    @staticmethod
    def create_trade_service() -> TradeService:
        """Cria uma instância do TradeService com todas as dependências"""
        # Cria o TradePlan padrão
        trade_plan = TradePlan(
            initial_balance=settings.default_trade_plan['initial_balance'],
            risk_per_trade=settings.default_trade_plan['risk_per_trade'],
            total_trades=settings.default_trade_plan['total_trades'],
            leverage=settings.default_trade_plan['leverage']
        )
        
        # Configura o repositório baseado nas configurações
        if settings.database_url:
            trade_repository = SQLAlchemyRepository(settings.database_url)
            unit_of_work = SQLAlchemyUnitOfWork(trade_repository)
        else:
            trade_repository = FileRepository(str(settings.trades_file))
            unit_of_work = FileUnitOfWork(trade_repository)
        
        # Cria o TradeService
        return TradeService(
            trade_plan=trade_plan,
            trade_repository=trade_repository,
            unit_of_work=unit_of_work
        )