#!/usr/bin/python3
# -*- coding: utf-8 -*-

from abc import ABCMeta
import threading


class SingletonABCMeta(ABCMeta):
    _instances = {}
    _lock = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._lock[cls] = threading.Lock()
            with cls._lock[cls]:
                if cls not in cls._instances:
                    cls._instances[cls] = super(SingletonABCMeta,
                                                cls).__call__(*args, **kwargs)
                    
        return cls._instances[cls]