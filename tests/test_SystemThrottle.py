# -*- coding: utf-8 -*-
""" TestSystemThrottle """
from oslash import Right, Left
from datetime import datetime, timedelta, timezone

from xross_common.SystemLogger import SystemLogger
from xross_common.SystemThrottle import SystemThrottle
from xross_common.XrossTestBase import XrossTestBase
from xross_common.CustomErrors import SystemThrottleError

THROTTLE_KEY = "TEST_ALGO"


class TestSystemThrottle(XrossTestBase):
    logger, test_handler = SystemLogger("TestSystemThrottle").get_logger()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sys_throttle = SystemThrottle()

    def test_check(self):
        # setup
        self.sys_throttle.set_throttle(THROTTLE_KEY, 10, 1)

        # check
        for i in range(9):
            self.assertEqual(Right("Success").value, self.sys_throttle.check(THROTTLE_KEY).value)

        result = self.sys_throttle.check(THROTTLE_KEY)
        self.assertEqual("SystemThrottle is detected. 10 times per 1 secs.", str(result.value))

    def test_check_raise_exception(self):
        # setup
        self.sys_throttle.set_throttle(THROTTLE_KEY, 10, 1)

        # check
        try:
            for i in range(10):
                self.sys_throttle.check_raise_exception(THROTTLE_KEY)
            self.fail()
        except SystemThrottleError as e:
            self.assertEqual("SystemThrottle is detected. 10 times per 1 secs.", str(e))
