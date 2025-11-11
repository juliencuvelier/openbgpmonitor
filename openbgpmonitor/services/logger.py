import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",  # Nom du fichier de log
    maxBytes=5000000,  # Taille maximale du fichier en octets
)

# Créer un logger spécifique pour le module principal
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)


def get_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
