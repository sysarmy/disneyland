import logging


def getLogger(name):
    """Crea un logger tuneado

    La idea era tener logs lo más detallados posibles, así que armamos un
    logger que escupa la info necesaria sobre cada paso.

    Args:
        name (str): nombre del logger.

    Returns:
        logging.Logger: logger tuneado.
    """

    logger = logging.getLogger(name)

    logformat = "%(asctime)s - %(name)s/%(funcName)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=logging.INFO, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )

    return logger
