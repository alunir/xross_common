# -*- coding: utf-8 -*-
""" TestSystemContext """
from xross_common.SystemContext import SystemContext

from xross_common.SystemLogger import SystemLogger
from xross_common.XrossTestBase import XrossTestBase

PARAM_KEY = "hoge"


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
        self.cxt.set({"hogemanager": HOGEMANAGER})

        # assert
        self.assertTrue(hasattr(self.cxt, "HOGEMANAGER"))

    def test_get(self):
        # setup
        self.test_set()

        # action
        mgr = self.cxt.get_str("HOGEMANAGER")

        # assert
        self.assertEqual("HOGEMANAGER", str(mgr.__name__))

    def test_has(self):
        # setup
        self.test_set()

        # action
        result = self.cxt.has("HOGEMANAGER")
        result2 = self.cxt.has("HOGEMANAGER2")

        # assert
        self.assertTrue(result)
        self.assertFalse(result2)

    def test_pop(self):
        # setup
        self.test_set()

        # action
        result = self.cxt.pop("HOGEMANAGER")

        # assert
        self.assertEqual(result, HOGEMANAGER)
        self.assertEqual("SystemContext{'debug': True}", str(self.cxt))

    def test_clear(self):
        # setup
        self.test_set()

        # action
        self.cxt.clear()

        # assert
        self.assertEqual("SystemContext{}", str(self.cxt))

    def test_get_mgr_fail(self):
        # setup
        self.test_set()

        # action
        try:
            self.XXX = self.cxt.get_str("XXX")
        except AttributeError as ex:
            self.assertEqual("'SystemContext' object has no attribute 'xxx'", str(ex))

    def test_get_int_fail_unless_set(self):
        self.assertEqual(0, self.cxt.get_int(PARAM_KEY))

    def test_get_int_fail_not_decimal(self):
        self.assertEqual(0, self.cxt.get_int(PARAM_KEY))
        self.cxt.increment(PARAM_KEY)
        self.assertEqual(1, self.cxt.get_int(PARAM_KEY))

        self.cxt.set({PARAM_KEY: "a"})

        try:
            self.cxt.get_int(PARAM_KEY)
            self.fail()
        except Exception as e:
            self.assertEqual("Value:a (Key:hoge) is not decimal", str(e))

    def test_increment(self):
        # setup
        self.cxt.set({PARAM_KEY: '99'})

        # action
        self.cxt.increment(PARAM_KEY)

        # assert
        self.assertEqual(100, self.cxt.get_int(PARAM_KEY))

        # action
        self.cxt.increment(PARAM_KEY, 100)

        # assert
        self.assertEqual(200, self.cxt.get_int(PARAM_KEY))


class HOGEMANAGER:
    pass


if __name__ == '__main__':
    TestSystemContext.do_test()
