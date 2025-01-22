import logging
from pathlib import Path
from config.settings import settings

# Configuração do logging
LOG_DIR = settings.data_dir / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = LOG_DIR / 'planotrade.log'

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('planotrade')

def configure_logging():
    """Configura o logging do sistema"""
    logger.info('Logging configurado com sucesso')
    logger.info(f'Logs serão salvos em: {LOG_FILE}')