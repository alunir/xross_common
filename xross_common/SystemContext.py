# -*- coding: utf-8 -*-
""" SystemContext """
from xross_common.DesignPattern import Singleton
from xross_common.SystemLogger import SystemLogger


class SystemContext(metaclass=Singleton):
    logger, test_handler = SystemLogger("SystemContext").get_logger()
    debug = False
    context = {}

    def __init__(self, debug=False):
        self.debug = debug

    def set(self, key: str, field: object) -> object:
        setattr(self, str(key).lower(), field)
        if self.debug:
            self.context.update({str(key).lower(): field})
            self.logger.debug("set:%s" % self.context)
        return field

    def get(self, key: str, default: object = None):
        if self.debug:
            self.logger.debug("get:%s" % self.context)
            self.context.get(str(key).lower(), default)
        return getattr(self, str(key).lower(), default)

    def get_int(self, key: str, default: int = None) -> int:
        if not str(self.get(key)).isdecimal():
            raise TypeError("%s is not decimal" % key)
        return self.get(key, default)

    def increment(self, key: str, delta: int = 1) -> int:
        new_val = int(self.get_int(key)) + delta
        self.set(key, new_val)
        return new_val
