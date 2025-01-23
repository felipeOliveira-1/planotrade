from typing import Optional
import typer
from models.trade import TradeStatus
from services.trade_service import TradeService
from core.factory import ServiceFactory
from core.logging import logger

app = typer.Typer()

@app.command()
def close(
    trade_id: int = typer.Argument(..., help="ID da operação a ser fechada"),
    price: float = typer.Argument(..., help="Preço de fechamento"),
    result: Optional[float] = typer.Option(None, help="Resultado da operação")
):
    """Fecha uma operação aberta"""
    try:
        trade_service: TradeService = ServiceFactory.create_trade_service()
        trade = trade_service.close_trade(trade_id, price, result)
        
        if trade.status == TradeStatus.CLOSED:
            logger.info(f"Operação {trade_id} fechada com sucesso!")
            logger.info(f"Resultado: {trade.result}")
            logger.info(f"Preço de fechamento: {trade.close_price}")
            logger.info(f"Data de fechamento: {trade.close_timestamp}")
        else:
            logger.error(f"Falha ao fechar operação {trade_id}")
            
    except Exception as e:
        logger.error(f"Erro ao fechar operação: {str(e)}")