#!/usr/bin/python3
# -*- coding: utf-8 -*-

from logging.handlers import RotatingFileHandler
from common.singleton import SingletonABCMeta
from common.config import Config

import os
import time
import logging


class Logger(object, metaclass=SingletonABCMeta):

    def __init__(self, logger_name="default"):
        log_time = time.strftime("%Y-%m-%d-%H%M", time.localtime())
        log_dir = Config().log_path
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except FileExistsError as err:
                self.logger.error(err)

        log_path = os.path.join(log_dir, f'{logger_name}_{log_time}.log')

        formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s")
        maxBytes = 500 * 1024 * 1024
        
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(Config().log_level)
        
        if Config().log_file:    
            handler = RotatingFileHandler(filename=log_path, maxBytes=maxBytes, backupCount=1, encoding="utf-8")
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        if Config().log_console:
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            console.setLevel(Config().log_level)
            self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

    def Debug(self, msg: str):
        self.logger.debug(msg)

    def Info(self, msg: str):
        self.logger.info(msg)

    def Warning(self, msg: str):
        self.logger.warning(msg)

    def Error(self, msg: str):
        self.logger.error(msg)

    def Critical(self, msg: str):
        self.logger.critical(msg)
