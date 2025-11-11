import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",  # Nom du fichier de log
    maxBytes=50000,  # Taille maximale du fichier en octets (ici, 5 Mo)
    backupCount=3,  # Nombre de fichiers de sauvegarde
)

# Créer un logger spécifique pour le module principal
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)


def get_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
