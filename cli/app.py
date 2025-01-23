import typer
from typing import Optional
from core.factory import ServiceFactory
from core.logging import logger
from models.trade import TradeStatus, TradeResult

app = typer.Typer()

@app.command()
def create(
    type: str = typer.Option(..., help="Tipo da operação (long/short)"),
    entry: float = typer.Option(..., help="Preço de entrada"),
    target: float = typer.Option(..., help="Preço alvo"),
    stop: float = typer.Option(..., help="Preço de stop"),
    leverage: int = typer.Option(2, help="Alavancagem (1-10)"),
    position_size: float = typer.Option(50.0, help="Tamanho da posição em % (1-100)")
):
    """Cria uma nova operação"""
    try:
        trade_service = ServiceFactory.create_trade_service()
        
        trade_data = {
            'type': type,
            'entry': entry,
            'target': target,
            'stop': stop,
            'leverage': leverage,
            'position_size': position_size
        }
        
        trade = trade_service.create_trade(trade_data)
        logger.info(f"Operação criada com sucesso: {trade}")
    except Exception as e:
        logger.error(f"Erro ao criar operação: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def list():
    """Lista operações abertas"""
    try:
        trade_service = ServiceFactory.create_trade_service()
        open_trades = trade_service.get_open_trades()
        
        if not open_trades:
            logger.info("Nenhuma operação aberta")
            return
            
        for i, trade in enumerate(open_trades):
            logger.info(f"\nOperação {i+1}:")
            logger.info(f"Tipo: {trade.type.value.upper()}")
            logger.info(f"Entrada: {trade.entry}")
            logger.info(f"Alvo: {trade.target}")
            logger.info(f"Stop: {trade.stop}")
            logger.info(f"Alavancagem: {trade.leverage}x")
            logger.info(f"Tamanho da posição: {trade.position_size_percent}%")
    except Exception as e:
        logger.error(f"Erro ao listar operações: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def close(
    trade_id: int = typer.Argument(..., help="ID da operação a ser fechada"),
    price: float = typer.Argument(..., help="Preço de fechamento"),
    result: Optional[float] = typer.Option(None, help="Resultado da operação")
):
    """Fecha uma operação aberta"""
    try:
        trade_service = ServiceFactory.create_trade_service()
        trade = trade_service.close_trade(trade_id, price, result)
        
        logger.info(f"Operação {trade_id} fechada com sucesso!")
        logger.info(f"Resultado: {trade.result}")
        logger.info(f"Preço de fechamento: {trade.close_price}")
        logger.info(f"Data de fechamento: {trade.close_timestamp}")
        
    except Exception as e:
        logger.error(f"Erro ao fechar operação: {str(e)}")
        logger.exception(e)
        raise typer.Exit(code=1)

def main():
    app()

@app.command()
def gui():
    """Inicia a interface gráfica"""
    from views.gui import start_gui
    from models.account import TradePlan
    from repositories.file_repository import FileRepository
    
    # Carrega o plano de trade
    # Carrega o plano de trade do arquivo
    repository = FileRepository('trades.json')
    trade_plan = repository.load_trade_plan()
    
    start_gui(trade_plan)

if __name__ == "__main__":
    main()