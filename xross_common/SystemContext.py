# -*- coding: utf-8 -*-
""" SystemContext """


def conv(key: str):
    return str(key).upper()


class SystemContext:
    logger, test_handler = None, None
    debug = False

    def __init__(self, debug=False):
        self.context = {}
        self.debug = debug
        if self.debug:
            from xross_common.SystemLogger import SystemLogger
            self.logger, test_handler = SystemLogger("SystemContext").get_logger()

    def set(self, dic: dict):
        for k, v in dic.items():
            setattr(self, str(k).upper(), v)
            self.context.update({conv(k): v})
        if self.debug:
            self.logger.debug("set:%s" % self.context)

    def get(self, key: str, default: object = None):
        if self.debug:
            self.logger.debug("get:%s" % self.context)
        self.context.get(conv(key), default)
        return getattr(self, conv(key), default)

    def has(self, key: str) -> bool:
        return key.upper() in self.context.keys()

    def pop(self, key: str):
        delattr(self, conv(key))
        return self.context.pop(conv(key))

    def clear(self):
        for k in self.context.keys():
            delattr(self, conv(k))
        self.context.clear()

    def get_int(self, key: str, default: int = 0) -> int:
        if not str(self.get(key, 0)).isdecimal():
            raise TypeError("Value:%s(Key:%s) is not decimal" % (self.get(key), key))
        return int(self.get(key, default))

    def increment(self, key: str, delta: int = 1) -> int:
        new_val = int(self.get_int(key)) + delta
        self.set({conv(key): new_val})
        return new_val

    def __iter__(self):
        return self.context.__iter__()

    def __repr__(self):
        return "SystemContext%s" % self.context

    def __len__(self):
        return len(self.context)
