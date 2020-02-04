import logging
import os
import uuid


class Logger:
    logger_name = 'testapi_logger'

    @staticmethod
    def create_logger(log_path):
        if not os.path.isdir(os.path.dirname(log_path)):
            os.mkdir(os.path.dirname(log_path))
        if os.path.isfile(log_path):
            os.remove(log_path)
        Logger.set_logger_name(f'{uuid.uuid4().hex[0:7]}_{Logger.logger_name}')
        file_handler = logging.FileHandler(log_path, 'a')
        formatter = logging.Formatter(u'%(asctime)s [%(levelname)-s]: %(message)s')
        file_handler.setFormatter(formatter)
        file_handler.set_name(Logger.logger_name)
        log = logging.getLogger(Logger.logger_name)
        for handler in log.handlers[:]:
            log.removeHandler(handler)
        log.addHandler(file_handler)
        log.setLevel(logging.DEBUG)

    @staticmethod
    def log_msg(msg):
        log = logging.getLogger(Logger.logger_name)
        log.debug(msg)

    @staticmethod
    def set_logger_name(name):
        Logger.logger_name = name
