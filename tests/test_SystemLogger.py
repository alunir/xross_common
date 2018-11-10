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
            ['Loaded SystemLogger for TestSystemLogger; LOGGER_LEVEL:DEBUG',
             'AlgoProcess is starting.',
             'hoge',
             'AlgoProcess is stopped.'],
            self.test_handler.formatted)


if __name__ == '__main__':
    TestSystemLogger.do_test()
