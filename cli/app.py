import typer
from typing import Optional
from core.factory import ServiceFactory
from core.logging import logger

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

def main():
    app()

if __name__ == "__main__":
    main()