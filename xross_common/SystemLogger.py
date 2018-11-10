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


class SystemLogger(logging.getLoggerClass()):
    def __init__(self, obj_name):
        """
        :param obj_name: str
        """
        super(logging.getLoggerClass(), self).__init__()
        self.cfg = SystemUtil()
        self.obj_name = str(obj_name)
        # MEMO: self.__class__.__name__ equals the name of the most offspring class.
        self.logger = logging.getLogger(self.obj_name)
        # MEMO: Defining root logger level is essential.
        self.logger.setLevel(logging.DEBUG)
        # MEMO: asyncio logger level is always DEBUG.
        logging.getLogger('asyncio').setLevel(logging.DEBUG)
        self.levelno = self.logger.getEffectiveLevel()

        self.format_string = "%(asctime)s [" + self.obj_name + ":%(levelname)s] (%(processName)s) %(message)s"
        self.formatter = logging.Formatter(self.format_string)

        self.test_handler = TestHandler(Matcher())

        # MEMO: In util module, SystemLogger will be failed in the day after start the process.
        handlers = list()
        handlers.append(self.setup_stream_handler())
        handlers.append(self.test_handler)

        if not self.cfg.env.is_unittest() and self.cfg.get_sysprop_or_env("IS_OUTPUT_TO_LOGFILE", bool):
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
        self.logger.info("Loaded SystemLogger for %s; LOGGER_LEVEL:%s"
                         % (self.obj_name, logging.getLevelName(self.levelno)))

    def get_logger(self):
        return self.logger, self.test_handler

    def setup_stream_handler(self):
        stream_handler = logging.StreamHandler()

        prefix = ""
        if not self.cfg.env.is_real():
            prefix = "DEMO:"
        format_string = prefix + self.format_string

        self.levelno = getattr(logging, self.cfg.get_sysprop_or_env("LOGGER_LEVEL"))
        stream_handler.setLevel(self.levelno)
        stream_handler.setFormatter(logging.Formatter(format_string))

        return stream_handler

    def setup_file_handler(self):
        # see http://www.python.ambitious-engineer.com/archives/725
        module_dir = self.cfg.get_env("DOCKER_DIST_DIR")
        logfile_dir = module_dir + '/' + self.cfg.get_sysprop("LOGFILE_PATH")
        os.makedirs(logfile_dir, exist_ok=True)
        if module_dir is None:
            raise Exception("setenv.sh seems not to be set.")
        logfile_name = 'latest' + self.cfg.get_sysprop("LOGFILE_NAME_EXT")
        file_handler = logging.handlers.WatchedFileHandler(logfile_dir + '/' + logfile_name, mode='a')

        file_handler.setLevel(getattr(logging, self.cfg.get_sysprop("LOGFILE_LEVEL")))
        file_handler.setFormatter(self.formatter)
        return file_handler

    def clear_file_handler(self):
        try:
            self.logger.removeHandler(self.file_handler)
        except AttributeError:
            AttributeError("file_handler is not found.")
