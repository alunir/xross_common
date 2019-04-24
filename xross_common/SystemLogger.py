# -*- coding: utf-8 -*-
""" SystemLogger """
# see https://docs.python.jp/3/howto/logging.html
# see https://docs.python.jp/3/howto/logging-cookbook.html#logging-cookbook
# see https://pythonhosted.org/logutils/testing.html
import logging
import logging.handlers

from logutils.testing import TestHandler, Matcher

from xross_common.SystemEnv import SystemEnv

TRACE_LEVEL_NUM = 5
VERBOSE_LEVEL_NUM = 15


class SystemLogger(logging.getLoggerClass()):
    env = SystemEnv.create()

    def __init__(self, obj_name, level="DEBUG"):
        """
        :param obj_name: str
        """
        super(logging.getLoggerClass(), self).__init__()
        self.obj_name = str(obj_name)
        # MEMO: self.__class__.__name__ equals the name of the most offspring class.
        self.logger = logging.getLogger(self.obj_name)

        self.format_string = "%(asctime)s [" + self.obj_name + ":%(levelname)s] (%(processName)s) %(message)s"
        self.formatter = logging.Formatter(self.format_string)
        self.test_handler = TestHandler(Matcher())

        self.levelno = None
        self.set_loglevel(level)

        self.register_handlers()

    def trace(self, message, *args, **kws):
        if self.logger.isEnabledFor(TRACE_LEVEL_NUM):
            self.logger._log(TRACE_LEVEL_NUM, message, args, **kws)

    def verbose(self, message, *args, **kws):
        if self.logger.isEnabledFor(VERBOSE_LEVEL_NUM):
            self.logger._log(VERBOSE_LEVEL_NUM, message, args, **kws)

    def set_loglevel(self, default_level):
        """
        MEMO: add custom logger levels
        ~ NOTSET, TRACE, DEBUG, VERBOSE, INFO, WARNING, ERROR, CRITICAL
        ~      0,     5,    10,      15,   20,      30,    40,       50

        LOG_LEVEL | SYS_ENV                          | Use for
                  | UNITTEST | LOCAL | DOCKER | PROD |
        ----------|----------|-------|--------|------|------------------------------------------------------------------
        NOTSET    |          |       |        |      | Do not use
        TRACE     | Y        |       |        |      | Private keys (e.g. SECRET_KEY, passwords...)
        DEBUG     | Y        | Y     |        |      | Tracking logs for LOCAL TEST
        VERBOSE   | Y        | Y     | Y      |      | Tracking logs for DEMO
        INFO      | Y        | Y     | Y      | Y    | Basic logs for PROD
        WARNING   | Y        | Y     | Y      | Y    | Application warning, still running
        ERROR     | Y        | Y     | Y      | Y    | Application warning, stop the system
        CRITICAL  | Y        | Y     | Y      | Y    | System disaster

        :param level: str
        :return: void
        """

        # MEMO: define custom logging levels
        for name, level in [('TRACE', TRACE_LEVEL_NUM), ('VERBOSE', VERBOSE_LEVEL_NUM)]:
            self.add_custom_logging_level(name, level)

        # MEMO: Defining root logger level is essential.
        self.levelno = logging.getLevelName(default_level)
        self.logger.setLevel(self.levelno)

        # MEMO: asyncio logger level is always DEBUG.
        logging.getLogger('asyncio').setLevel(logging.DEBUG)

    def add_custom_logging_level(self, name, level):
        """
        :param name: str
        :param level: str
        :return: void
        """
        logging.addLevelName(level, name)
        setattr(self.logger, name.lower(), getattr(self, name.lower()))

    def register_handlers(self):
        # MEMO: In util module, SystemLogger will be failed in the day after start the process.
        handlers = list()
        handlers.append(self.setup_stream_handler())
        handlers.append(self.test_handler)

        for orig_handler in handlers:
            self.logger.addHandler(orig_handler)
        self.logger.info("Loaded SystemLogger LOGGER_LEVEL:%s" % logging.getLevelName(self.levelno))

    def get_logger(self):
        return self.logger, self.test_handler

    def setup_stream_handler(self):
        stream_handler = logging.StreamHandler()

        prefix = ""
        if not self.env.is_real():
            prefix = "DEMO:"
        format_string = prefix + self.format_string

        stream_handler.setLevel(self.levelno)
        stream_handler.setFormatter(logging.Formatter(format_string))

        return stream_handler

    def clear_file_handler(self):
        try:
            self.logger.removeHandler(self.file_handler)
        except AttributeError:
            AttributeError("file_handler is not found.")
