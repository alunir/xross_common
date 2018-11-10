# -*- coding: utf-8 -*-
""" SystemContext """
from xross_common.DesignPattern import Singleton
from xross_common.SystemLogger import SystemLogger


class SystemContext(metaclass=Singleton):
    logger, test_handler = SystemLogger("SystemContext").get_logger()

    def __init__(self):
        pass

    def set_field(self, key, field):
        """
        :param key: str
        :param field: something
        :return: field
        """
        setattr(self, str(key).lower(), field)
        return field

    def get_field(self, key, default=0):
        """
        :param key: str
        :param default: int
        :return: field
        """
        return getattr(self, str(key).lower(), default)

    def increment_field(self, key):
        """
        :param key: str
        :return: field
        """
        new_val = self.get_field(key) + 1
        self.set_field(key, new_val)
        return new_val
