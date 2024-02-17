import logging


class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s %(message)s')
        self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)


logger: Logger = Logger()

__all__ = [logger]
