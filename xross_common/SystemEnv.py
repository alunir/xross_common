# -*- coding: utf-8 -*-
""" SystemEnv """
import os
import sys
import ast
from enum import Enum


class SystemEnv(Enum):
    # Running on the server
    PROD = 'prod'
    # Running on Docker Container
    DOCKER = 'docker'
    # Running by 'make test' on the local
    LOCAL = 'local'
    # Running by unittests on the local
    UNITTEST = 'unittest'
    UNKNOWN = 'unknown'

    @staticmethod
    def create():
        if ast.literal_eval(os.environ.get("IS_UNITTEST", 'False')) \
                or 'pycharm' in sys.argv[0] or 'setup.py' in sys.argv[0] or '.pyenv/versions' in sys.executable:
            return SystemEnv.UNITTEST
        elif ast.literal_eval(os.environ.get("IS_LOCAL", 'False')):
            return SystemEnv.LOCAL
        elif ast.literal_eval(os.environ.get("IS_DOCKER", 'False')):
            return SystemEnv.DOCKER
        elif "REAL=True" in sys.argv:
            return SystemEnv.PROD
        else:
            return SystemEnv.UNKNOWN

    def is_real(self):
        return self is SystemEnv.PROD

    def is_docker(self):
        return self is SystemEnv.DOCKER

    def is_unittest(self):
        return self is SystemEnv.UNITTEST

    def is_local(self):
        return self is SystemEnv.LOCAL
