# -*- coding: utf-8 -*-
""" SystemThrottle """
import time
from collections import namedtuple, deque
from datetime import datetime

import pykka
from oslash import Right, Left
from xross_common.CustomErrors import SystemThrottleError
from xross_common.DesignPattern import Singleton
from xross_common.Dotdict import Dotdict
from xross_common.SystemLogger import SystemLogger

Throttle = namedtuple("Throttle", ("limit", "interval"))


class ActorCounter(pykka.ThreadingActor, metaclass=Singleton):
    counter = {}

    def __init__(self):
        super().__init__()
        # MEMO: if the parent object was killed, this object is also killed.
        self.use_daemon_thread = True

    def on_receive(self, message):
        action_type = message['action']
        key = message['key']
        if action_type == 'initialize':
            self.counter.update({key: deque(maxlen=message['limit'])})
        elif action_type == 'list':
            return list(self.counter[key])
        elif action_type == 'put':
            self.counter[key].append(message['now'])
        else:
            raise ValueError(message)


class SystemThrottle(metaclass=Singleton):
    logger, test_handler = SystemLogger("SystemThrottle").get_logger()
    timemgr = None
    throttle = {}
    counter = ActorCounter().start()

    def __init__(self, timemgr=None):
        super().__init__()
        self.timemgr = timemgr
        if not self.timemgr:
            from datetime import datetime

    def __get_now(self):
        if not self.timemgr:
            return datetime.utcnow().timestamp()
        else:
            return self.timemgr.get_systemtimestamp().to_unix_timestamp()

    def check(self, key: str) -> "Either":
        self.counter.ask({'action': 'put', 'key': key, 'now': self.__get_now()})

        l = self.counter.ask({'action': 'list', 'key': key})
        throttle = self.throttle[key]
        if len(l) < throttle.limit:
            return Right("Success")
        elif l[-throttle.limit] + throttle.interval < self.__get_now():
            return Right("Success")
        else:
            msg = "SystemThrottle is detected. %s times per %s secs." % (throttle.limit, throttle.interval)
            self.logger.warning(msg)
            return Left(msg)

    def check_raise_exception(self, key: str) -> None:
        result = self.check(key)
        if isinstance(result, Left):
            raise SystemThrottleError(result.value)

    def check_and_wait(self, key:str) -> None:
        self.check(key)
        time.sleep(l[-throttle.limit] + throttle.interval - self.__get_now())

    def set_throttle(self, key: str, limit: int, interval: int) -> None:
        self.throttle.update({key: Throttle(limit, interval)})
        self.counter.ask({'action': 'initialize', 'key': key, 'limit': limit})

    def get_throttle(self, key: str) -> int:
        return self.throttle[key]

    def clear_throttle_for_test(self, key=None) -> None:
        if not key:
            self.throttle.clear()
        else:
            self.throttle[key].clear()
