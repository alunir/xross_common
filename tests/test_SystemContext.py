# -*- coding: utf-8 -*-
""" TestSystemContext """
from xross_common.SystemContext import SystemContext

from xross_common.SystemLogger import SystemLogger
from xross_common.XrossTestBase import XrossTestBase


class TestSystemContext(XrossTestBase):
    logger, test_handler = SystemLogger("TestSystemContext").get_logger()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.cxt = SystemContext(debug=True)

    def tearDown(self):
        self.cxt = None

    def test_set(self):
        # action
        self.cxt.set("HOGEMANAGER", HOGEMANAGER)

        # assert
        self.assertTrue(hasattr(self.cxt, "hogemanager"))

    def test_get(self):
        # setup
        self.test_set()

        # action
        mgr = self.cxt.get("HOGEMANAGER")

        # assert
        self.assertEqual("HOGEMANAGER", str(mgr.__name__))

    def test_get_mgr_fail(self):
        # setup
        self.test_set()

        # action
        try:
            self.XXX = self.cxt.get("XXX")
        except AttributeError as ex:
            self.assertEqual("'SystemContext' object has no attribute 'xxx'", str(ex))

    def test_increment(self):
        PARAM_KEY = "hoge"

        # setup
        self.cxt.set(PARAM_KEY, 99)

        # action
        self.cxt.increment(PARAM_KEY)

        # assert
        self.assertEqual(100, self.cxt.get(PARAM_KEY))

        # action
        self.cxt.increment(PARAM_KEY, 100)

        # assert
        self.assertEqual(200, self.cxt.get(PARAM_KEY))


class HOGEMANAGER:
    pass


if __name__ == '__main__':
    TestSystemContext.do_test()
