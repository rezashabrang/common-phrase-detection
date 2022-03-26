"""Logger definitions."""
import logging


def get_logger():
    """Getting logger."""
    # Configuring Logger
    logging.root.setLevel(logging.NOTSET)
    logger = logging.getLogger("phrase_logger")

    # Create handler
    s_handler = logging.StreamHandler()
    s_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    s_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    s_handler.setFormatter(s_format)

    logger.addHandler(s_handler)

    return logger
