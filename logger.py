# pythonのloggingについてのメモ
# https://qiita.com/studio_haneya/items/469f3cf534bf68541a77

from logging import Formatter, handlers, StreamHandler, getLogger, NullHandler
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL


class Logger:
    def __init__(self, name=__name__, filename="", level=DEBUG, valid=True):
        assert isinstance(filename, str), 'filename must be string: {}'.format(filename)

        self.logger = getLogger(name)
        self.logger.setLevel(level)
        formatter = Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")

        # stdout
        if valid == True:
            handler = StreamHandler()
        else:
            handler = NullHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # file
        if filename != "":
            handler = handlers.RotatingFileHandler(filename=filename,
                                                   maxBytes=1048576,
                                                   backupCount=3)
            handler.setLevel(level)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
