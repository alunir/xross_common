# -*- coding: utf-8 -*-
""" TestSystemLogger """
import multiprocessing

from xross_common.SystemLogger import SystemLogger
from xross_common.XrossTestBase import XrossTestBase


class TestSystemLogger(XrossTestBase):
    logger, test_handler = SystemLogger("TestSystemLogger").get_logger()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tearDown(self):
        self.test_handler.flush()

    def test_log_once(self):
        # action
        self.logger.info("hoge")

        # assert
        self.assertEqual(["hoge"], self.test_handler.formatted)

    def test_log_twice(self):
        # action
        self.logger.info("hoge1")
        self.logger.info("hoge2")

        # assert
        self.assertEqual(["hoge1", "hoge2"], self.test_handler.formatted)

    def test_log_multi_process(self):
        # action
        self.logger.info("AlgoProcess is starting.")
        algo_proc = multiprocessing.Process(target=self.logger.info("hoge"), name="AlgoProcess")
        algo_proc.start()
        algo_proc.join()
        self.logger.info("AlgoProcess is stopped.")

        # assert
        self.assertEqual(
            ['AlgoProcess is starting.',
             'hoge',
             'AlgoProcess is stopped.'],
            self.test_handler.formatted)

    def test_custom_log(self):
        self.logger.trace("TRACE log is available.")
        self.assertEqual(
            ['Loaded SystemLogger LOGGER_LEVEL:DEBUG'],
            self.test_handler.formatted
        )

        self.logger.verbose("VERBOSE log is available.")
        self.assertEqual(
            ['Loaded SystemLogger LOGGER_LEVEL:DEBUG', 'VERBOSE log is available.'],
            self.test_handler.formatted
        )

    def test_custom_log_set_logger_level(self):
        logger, test_handler = SystemLogger("TestSystemLogger", level="TRACE").get_logger()
        logger.trace("TRACE log is available.")

        self.assertEqual(
            ['Loaded SystemLogger LOGGER_LEVEL:TRACE', 'TRACE log is available.'],
            test_handler.formatted
        )

        logger.verbose("VERBOSE log is available.")
        self.assertEqual(
            ['Loaded SystemLogger LOGGER_LEVEL:TRACE',
             'TRACE log is available.',
             'VERBOSE log is available.'],
            test_handler.formatted
        )


if __name__ == '__main__':
    TestSystemLogger.do_test()
