# -*- coding: utf-8 -*-
""" TestXrossTestBase """
from xross_common.XrossTestBase import XrossTestBase
from xross_common.SystemLogger import SystemLogger


class TestXrossTestBase(XrossTestBase):
    logger, test_handler = SystemLogger("TestTestBase").get_logger()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test(self):
        pass


if __name__ == '__main__':
    XrossTestBase.do_test()
