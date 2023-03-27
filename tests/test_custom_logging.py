import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.custom_logger import CustomLogger

CustomLogger.setup_custom_logging()
import logging

def log_messages():
    logging.debug("Mensaje de depuración")
    logging.info("Mensaje informativo")
    logging.warning("Mensaje de advertencia")
    logging.error("Mensaje de error")
    logging.critical("Mensaje crítico")

if __name__ == "__main__":
    log_messages()
