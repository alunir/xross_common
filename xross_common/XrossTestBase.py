# -*- coding: utf-8 -*-
""" XrossTestBase """
import time
import logging
import unittest
from functools import wraps
from collections import OrderedDict
from xross_common.SystemLogger import SystemLogger
from xross_common.SystemUtil import SystemUtil


class XrossTestBase(unittest.TestCase):
    _logger, _test_handler = SystemLogger("XrossTestBase").get_logger()
    _logger.setLevel(logging.DEBUG)
    cxt = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg = SystemUtil()
        self._logger.info("XrossTestBase has been loaded.")

    def setUp(self):
        super().setUp()
        self._logger.addHandler(self._test_handler)
        self._logger.debug("XrossTestBase.setUp()")

    def tearDown(self):
        super().tearDown()
        self._logger.debug("XrossTestBase.tearDown()")
        self._logger.removeHandler(self._test_handler)
        self._test_handler.flush()

    # noinspection PyMethodParameters
    def do_test():
        unittest.main()

    def assertSelectSetEqual(self, expected, actual):
        sorted_expect_list = sorted(expected, key=lambda x: x['timestamp'])
        sorted_actual_list = sorted(actual, key=lambda x: x['timestamp'])
        for d1, d2 in zip(sorted_expect_list, sorted_actual_list):
            try:
                self.assertDictEqual(
                    OrderedDict(sorted(d1.items(), key=lambda x: x[0])),
                    OrderedDict(sorted(d2.items(), key=lambda x: x[0]))
                )
            except AssertionError as e:
                self._logger.warning("expected_element: %s, but actual_element: %s" % (str(d1), str(d2)))
                self._logger.warning("expected: %s, but actual: %s" % (str(sorted_expect_list), str(sorted_actual_list)))
                raise e

    def assertRegexList(self, expected_regex_list, actual_list):
        if len(actual_list) != len(expected_regex_list):
            self.fail("Length of lists doesn't match. %s!=%s" % (len(expected_regex_list), len(actual_list)))
        for text, regex in zip(actual_list, expected_regex_list):
            self.assertRegex(text, regex)

    def assertObject(self, expect, actual):
        # print("assertObject is scanning in %s" % dir(expect))
        for e, a in zip(dir(expect), dir(actual)):
            if not e.startswith("_") and not a.startswith("_") and not callable(getattr(expect, e)):
                try:
                    self.assertEqual(getattr(expect, e), getattr(actual, a))
                except AssertionError as ex:
                    print("AssertionError has occurred comparing between %s" % e)
                    raise ex

    @staticmethod
    def retry(exception_to_check, tries=4, delay=1, backoff=2, logger=None):
        """Retry calling the decorated function using an exponential backoff.

        http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
        original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

        :param exception_to_check: the exception to check. may be a tuple of
            exceptions to check
        :type exception_to_check: Exception or tuple
        :param tries: number of times to try (not retry) before giving up
        :type tries: int
        :param delay: initial delay between retries in seconds
        :type delay: int
        :param backoff: backoff multiplier e.g. value of 2 will double the delay
            each retry
        :type backoff: int
        :param logger: logger to use. If None, print
        :type logger: logging.Logger instance
        """
        def deco_retry(f):

            @wraps(f)
            def f_retry(*args, **kwargs):
                self, mtries, mdelay = args[0], tries, delay
                while mtries > 0:
                    try:
                        self.setUp()
                        return f(*args, **kwargs)
                    except exception_to_check as e:
                        msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                        if logger:
                            logger.warning(msg)
                        else:
                            print(msg)
                        time.sleep(mdelay)
                        mtries -= 1
                        mdelay *= backoff
                    finally:
                        self.tearDown()
                if mtries == 0:
                    self.fail()
                return f(*args, **kwargs)

            return f_retry  # true decorator

        return deco_retry
