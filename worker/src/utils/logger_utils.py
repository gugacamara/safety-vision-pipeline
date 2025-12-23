import logging

"""
Configura e retorna um logger para uso na aplicação.
Args:
    name (str): Nome do logger.
    level (int): Nível de log (default: logging.INFO).
Returns:
    logging.Logger: Logger configurado.
"""
def get_logger(name: str = "worker", level: int = logging.INFO):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger