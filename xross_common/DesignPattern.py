# -*- coding: utf-8 -*-
""" DesignPattern """
from abc import ABC, ABCMeta, abstractmethod


class Singleton(type):
    """
    To use this metaclass, declare __metaclass__ in your class, like following :

    class Singleton:
        __metaclass__ = SingletonType

    When Singleton is declared, SingletonType.__new__ will be executed.

    See : https://media.accel-brain.com/python3-singleton/
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class IFactory(metaclass=ABCMeta):
    @abstractmethod
    def create(self):
        pass


class IProduct(metaclass=ABCMeta):
    @abstractmethod
    def use(self, *args):
        pass


class ISingletonFactory(ABC, IFactory, Singleton):
    @abstractmethod
    def create(self):
        pass


class ISingletonProduct(ABC, IProduct, Singleton):
    @abstractmethod
    def use(self):
        pass
