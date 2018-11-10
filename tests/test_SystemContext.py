# -*- coding: utf-8 -*-
""" TestSystemContext """
from xross_common.SystemContext import SystemContext

from xross_common.SystemLogger import SystemLogger
from xross_common.XrossTestBase import XrossTestBase


class TestSystemContext(XrossTestBase):
    logger, test_handler = SystemLogger("TestSystemContext").get_logger()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cxt = SystemContext()

    def test_set_field(self):
        # action
        self.cxt.set_field("HOGEMANAGER", HOGEMANAGER)

        # assert
        self.assertTrue(hasattr(self.cxt, "hogemanager"))

    def test_get_field(self):
        # setup
        self.test_set_field()

        # action
        mgr = self.cxt.get_field("HOGEMANAGER")

        # assert
        self.assertEqual("HOGEMANAGER", str(mgr.__name__))

    def test_get_mgr_fail(self):
        # setup
        self.test_set_field()

        # action
        try:
            self.XXX = self.cxt.get_field("XXX")
        except AttributeError as ex:
            self.assertEqual("'SystemContext' object has no attribute 'xxx'", str(ex))


class HOGEMANAGER:
    pass


if __name__== '__main__':
    TestSystemContext.do_test()
