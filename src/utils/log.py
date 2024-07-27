import logging
import os
import time
from datetime import datetime
from functools import wraps

from src.configs.config_loader import AppFolders


def print_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        Log.info(f'Execution time of {func.__name__}: {execution_time:.4f} seconds')
        return result

    return wrapper


class Log:
    filename = None
    logger = logging.getLogger(os.environ.get('PYTEST_XDIST_WORKER', __name__))
    print(f'worker = {logger}')

    @classmethod
    def get_logger(cls):
        if len(cls.logger.handlers) == 0:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter('%(asctime)s %(name)s %(levelname)-8s %(message)s')
            )
            handler.setLevel(logging.DEBUG)
            cls.logger.addHandler(handler)
            cls.logger.setLevel(logging.DEBUG)
            cls.filename = os.path.join(
                os.path.join(AppFolders.TESTS_PATH, f'logs{os.sep}'),
                datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H%M%S')
                + cls.logger.name
                + '.log',
            )
            if not os.path.exists(os.path.dirname(cls.filename)):
                os.makedirs(os.path.dirname(cls.filename))
            fh = logging.FileHandler(cls.filename)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s %(name)s %(levelname)-8s %(message)s'
            )
            fh.setFormatter(formatter)
            cls.logger.addHandler(fh)
        return cls.logger

    @classmethod
    def info(cls, message):
        cls.get_logger().info(message)

    @classmethod
    def debug(cls, message):
        cls.get_logger().debug('\t\t' + message)

    @classmethod
    def error(cls, message):
        cls.get_logger().error(message)

    @classmethod
    def warning(cls, message):
        cls.get_logger().warning(message)
