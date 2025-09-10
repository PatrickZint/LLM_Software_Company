import logging


def setup_logger(logging_config):
    """
    Set up the application's logging based on configuration.

    Args:
        logging_config (dict): Dictionary containing logging parameters such as level and output file.
    """
    level = logging_config.get('level', 'INFO').upper()
    log_file = logging_config.get('file', 'app.log')
    
    # Set up basic configuration for logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
