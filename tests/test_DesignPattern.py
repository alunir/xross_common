# -*- coding: utf-8 -*-
""" TestDesignPattern """
from xross_common.DesignPattern import Singleton
from xross_common.XrossTestBase import XrossTestBase


class SingletonA(metaclass=Singleton):
    pass


class SingletonB(metaclass=Singleton):
    pass


class TestSingletonType(XrossTestBase):
    def test_singletonA(self):
        print("test_singletonA.A:" + str(id(SingletonA())))
        print("test_singletonA.A:" + str(id(SingletonA())))
        self.assertTrue(id(SingletonA()) == id(SingletonA()))

    def test_singletonB(self):
        print("test_singletonB.B:" + str(id(SingletonB())))
        print("test_singletonB.B:" + str(id(SingletonB())))
        self.assertTrue(id(SingletonB()) == id(SingletonB()))

    def test_singletonAB(self):
        print("test_singletonAB.A:" + str(id(SingletonA())))
        print("test_singletonAB.B:" + str(id(SingletonB())))
        self.assertFalse(id(SingletonA()) == id(SingletonB()))


if __name__ == '__main__':
    TestSingletonType.do_test()
    # MEMO: do not forget adding another class do_test().
    # TestAnotherClass.do_test()
