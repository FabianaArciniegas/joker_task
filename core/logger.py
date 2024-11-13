import logging


def logger_api(id_logger_: str):
    logger = logging.getLogger(id_logger_)

    # Avoid reconfiguring the logger if it has already been configured
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        # Log format
        formatter = logging.Formatter(f'%(asctime)s - %(levelname)s: {id_logger_} - %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')

        # StreamHandler to print to console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # FileHandler to save logs to a file
        file_handler = logging.FileHandler("logs/data_processor.log")
        file_handler.setFormatter(formatter)

        # Add both handlers
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    return logger
