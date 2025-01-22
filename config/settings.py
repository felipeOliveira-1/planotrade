from pathlib import Path
import os

# Configurações do sistema
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Caminho para o arquivo de trades
TRADES_FILE = DATA_DIR / 'trades.json'

# Configurações de banco de dados
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DATA_DIR}/trades.db')

# Configurações padrão do TradePlan
DEFAULT_TRADE_PLAN = {
    'initial_balance': 10000.0,
    'risk_per_trade': 1.0,
    'total_trades': 100,
    'leverage': 1
}

class Settings:
    def __init__(self):
        self.base_dir = BASE_DIR
        self.data_dir = DATA_DIR
        self.trades_file = TRADES_FILE
        self.database_url = DATABASE_URL
        self.default_trade_plan = DEFAULT_TRADE_PLAN

settings = Settings()