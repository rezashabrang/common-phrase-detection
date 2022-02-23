import logging


def get_logger():
    """Getting logger"""
    # Configuring Logger
    logger = logging.getLogger('phrase_logger')

    # Create handler
    s_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    s_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    s_handler.setFormatter(s_format)

    logger.addHandler(s_handler)

    return logger
