# -*- coding: utf-8 -*-
""" SystemLogger """
# see https://docs.python.jp/3/howto/logging.html
# see https://docs.python.jp/3/howto/logging-cookbook.html#logging-cookbook
# see https://pythonhosted.org/logutils/testing.html
import os
import logging
import logging.handlers

from logutils.testing import TestHandler, Matcher
from multiprocessing_logging import MultiProcessingHandler

from xross_common.SystemUtil import SystemUtil

TRACE_LEVEL_NUM = 5
VERBOSE_LEVEL_NUM = 15


class SystemLogger(logging.getLoggerClass()):
    def __init__(self, obj_name, level="DEBUG"):
        """
        :param obj_name: str
        """
        super(logging.getLoggerClass(), self).__init__()
        self.cfg = SystemUtil()
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
        logger_level = self.cfg.get_env("LOGGER_LEVEL", default=default_level)
        self.levelno = logging.getLevelName(logger_level)
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

        if not self.cfg.env.is_unittest() and self.cfg.get_env("IS_OUTPUT_TO_LOGFILE", default=False, type=bool):
            handlers.append(self.setup_file_handler())

        if self.cfg.env.is_real():
            for i, orig_handler in enumerate(handlers):
                handler = MultiProcessingHandler(
                    'mp-handler-{0}'.format(i), sub_handler=orig_handler
                )
                self.logger.addHandler(handler)
            self.logger.info("Initialized SystemLogger for %s with %s MultiProcessingHandler"
                             % (self.obj_name, len(handlers)))
        else:
            for orig_handler in handlers:
                self.logger.addHandler(orig_handler)
        self.logger.info("Loaded SystemLogger LOGGER_LEVEL:%s" % logging.getLevelName(self.levelno))

    def get_logger(self):
        return self.logger, self.test_handler

    def setup_stream_handler(self):
        stream_handler = logging.StreamHandler()

        prefix = ""
        if not self.cfg.env.is_real():
            prefix = "DEMO:"
        format_string = prefix + self.format_string

        stream_handler.setLevel(self.levelno)
        stream_handler.setFormatter(logging.Formatter(format_string))

        return stream_handler

    def setup_file_handler(self):
        # see http://www.python.ambitious-engineer.com/archives/725
        module_dir = self.cfg.get_env("DOCKER_DIST_DIR")
        logfile_dir = module_dir + '/' + self.cfg.get_env("LOGFILE_PATH", "logs")
        os.makedirs(logfile_dir, exist_ok=True)
        if module_dir is None:
            raise Exception("setenv.sh seems not to be set.")
        logfile_name = 'latest' + self.cfg.get_env("LOGFILE_NAME_EXT", ".log")
        file_handler = logging.handlers.WatchedFileHandler(logfile_dir + '/' + logfile_name, mode='a')

        file_handler.setLevel(self.levelno)
        file_handler.setFormatter(self.formatter)
        return file_handler

    def clear_file_handler(self):
        try:
            self.logger.removeHandler(self.file_handler)
        except AttributeError:
            AttributeError("file_handler is not found.")
