import logging

loggers = dict()


def setup_custom_logger(name):
    if loggers.get(name):
        return loggers.get(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    loggers[name] = logger
    return logger
