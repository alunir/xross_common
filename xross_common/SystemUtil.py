# -*- coding: utf-8 -*-
""" SystemUtil """
import os
import sys
import ast
import json
import configparser
from munch import Munch
from xross_common.DesignPattern import Singleton
from xross_common.SystemEnv import SystemEnv
from xross_common.SystemContext import SystemContext
# To avoid the circular reference, SystemLogger cannot be imported. This class is compiled at first.


def to_munch(dic):
    """
    :param dic: String, String
    :return: Munch (all keys are converted upper.)
    """
    return Munch((k.upper(), v) for k, v in dic.items())


def args_parser(lst):
    """
    :param list(String): contains args ex) TEST_MODE=True
    :return: Munch
    """
    result = dict()
    for e in lst:
        if "=" not in e:
            print("The arguments should be obeyed with the map format such as TEST_MODE=True, but was " + e)
            continue
        key, value = e.split("=")
        result.update({key: value})
    # return Munch(result)
    return result


class SystemUtil(metaclass=Singleton):
    env = SystemEnv.create()
    cfg = SystemContext()
    ini_files = []

    def __init__(self):
        super().__init__()
        base_dir = os.path.normpath(os.path.dirname(__file__) + "/../")
        if self.env.is_local() and not self.is_env("DOCKER_DIST_DIR"):
            self.set_env("DOCKER_DIST_DIR", base_dir)
        self.update(os.environ.get("DOCKER_DIST_DIR") + "/" + os.environ.get("CONFIG_PATH"))

    def update(self, full_path):
        cfg_parser = configparser.ConfigParser()
        cfg_path = os.path.normpath(full_path)
        self.ini_files = [cfg_path + "/" + f for f in os.listdir(cfg_path) if f.endswith(".ini")]
        if self.ini_files is []:
            raise ValueError("Failed to load ini files. see cfg_path %s" % cfg_path)
        cfg_parser.read(self.ini_files)

        if self.env.is_real():
            self.cfg.set(cfg_parser["DEFAULT_GLOBAL_CONFIG"])
        else:
            self.cfg.set(cfg_parser["TEST_DEFAULT_GLOBAL_CONFIG"])

        # MEMO: arguments should be override to config.
        self.cfg.set(args_parser(sys.argv[1:]))

    def get_sysprop_or_env(self, key, type=str):
        """
        If key is in sysprop, the value will be returned. Then key will be searched in environment variables.
        Otherwise this method will return None.
        sysprop are prior to environment variables.
        :param key: str
        :param type: type
        :return: type
        """
        result = None
        if type == str:
            if self.get_sysprop(str(key)) is None:
                result = self.get_env(str(key))
            else:
                result = self.get_sysprop(str(key))
        if type == bool:
            if self.get_sysprop(str(key)) is None:
                result = ast.literal_eval(self.get_env(str(key)))
            else:
                result = ast.literal_eval(self.get_sysprop(str(key)))
        return result

    def get_sysprop(self, key, default=None, type=str):
        """
        :param key: str
        :return: str
        """
        if not self.cfg.has(key):
            return None
        val = self.cfg.get(str(key), default=default)
        if type == dict:
            if "{" in val and "}" in val:
                val = json.loads(val.replace("'", "\""))
            if "," in val:
                if "[" == val[0] and "]" == val[-1]:
                    val = val[1:-2]
                val = val.replace(" ", "").split(",")
        if type == bool:
            val = ast.literal_eval(val)
        return val

    def get_all_sysprop(self):
        """
        :return: Munch
        """
        return self.cfg

    def set_sysprop(self, key, value):
        """
        :param key: str
        :param value: str
        :return: void
        """
        if type(key) is not str:
            raise TypeError("key is not str but was " + str(type(key)))
        if type(value) is not str:
            raise TypeError("value is not str but was " + str(type(value)))
        self.cfg.set({key: value})

    def remove_sysprop(self, key):
        """
        :param key: str
        :return: void
        """
        if str(key) not in self.cfg:
            raise ValueError("GLOBAL_CONFIG_ORDER doesn't contain key : " + str(key))
        self.cfg.pop(key)

    def get_env(self, key, default=None, type=str):
        """
        :param key:
        :param default: None
        :return: void
        """
        val = os.environ.get(str(key), default)
        if type == bool:
            if val is None:
                val = False
            else:
                val = ast.literal_eval(str(val))
        return val

    @staticmethod
    def get_all_env_for_test():
        """
        :return: environ
        """
        return os.environ

    def set_env(self, key, value):
        """
        :param key:
        :param value:
        :return:
        """
        if type(key) is not str:
            raise TypeError("key is not str but was " + str(type(key)))
        if type(value) is not str:
            raise TypeError("value is not str but was " + str(type(value)))
        os.environ.update({key: value})

    def remove_env(self, key):
        """
        :param key: str
        :return: void
        """
        if not self.is_env(key):
            raise ValueError("ENVIRONMENT VALUES doesn't contain key : " + str(key))
        os.environ.pop(str(key))

    def is_env(self, key: str) -> bool:
        return str(key) in os.environ

    # TODO: Implement Global Config Order
    @DeprecationWarning
    def overwrite_gcfg_for_test(self, key, value):
        """
        :str key
        :str value
        """
        _value = self.cfg[str(key)]
        self.cfg.append(set(str(key) + ":" + str(value)), str)
        if _value is None:
            print("GLOBAL_CONFIG_ORDER." + str(key) + " was added, " + str(value))
        else:
            print("GLOBAL_CONFIG_ORDER." + str(key) + " was replaced, before:" + _value + "->" + str(value))
        os.environ.putenv(str(key), str(value))

    def recreate_gcfg_for_test(self, gcfg):
        raise NotImplementedError

    def replace_gcfg_for_test(self, key):
        raise NotImplementedError

    def clear_gcfg_for_test(self):
        """
        :return: void
        """
        self.cfg.clear()
