# -*- coding: utf-8 -*-
""" SystemContext """
from xross_common.Dotdict import Dotdict


def conv(key: str):
    return str(key).upper()


class SystemContext(Dotdict):
    logger, test_handler = None, None
    debug = False

    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug
        if self.debug:
            from xross_common.SystemLogger import SystemLogger
            self.logger, test_handler = SystemLogger("SystemContext").get_logger()

    def set(self, dic: dict):
        for k, v in dic.items():
            setattr(self, str(k).upper(), v)
        if self.debug:
            self.logger.debug("set:%s" % self)

    def __get(self, key: str, default: object = None):
        if self.debug:
            self.logger.debug("get:%s" % self)
        item = getattr(self, conv(key))
        return item if item else default

    def has(self, key: str) -> bool:
        return key.upper() in self.keys()

    def get_int(self, key: str, default: int = 0) -> int:
        if not str(self.__get(key, default=0)).isdecimal():
            raise TypeError("Value:%s (Key:%s) is not decimal" % (self.__get(key), key))
        return int(self.__get(key, default=default))

    def get_str(self, key: str, default: str = "") -> str:
        return self.__get(key, default)

    def increment(self, key: str, delta: int = 1) -> int:
        new_val = int(self.get_int(key)) + delta
        self.set({conv(key): new_val})
        return new_val

    def __repr__(self):
        return "SystemContext%s" % super().__repr__()
