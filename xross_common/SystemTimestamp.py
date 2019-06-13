# -*- coding: utf-8 -*-
""" SystemTimestamp """
from datetime import datetime, timezone

import dateutil.tz

from xross_common.SystemUtil import SystemUtil

FORMAT_DEFAULT = "%Y-%m-%d %H:%M:%S.%f"
FORMAT_ISO8601 = "%Y-%m-%dT%H:%M:%S.%fZ"


class SystemTimestamp:
    timestamp_format = SystemUtil().get_env("DATE_FORMAT", default=FORMAT_DEFAULT)

    def __init__(self, *args):
        self.timestamp = ()
        if args == ():
            self.reload()
        else:
            self.timestamp = args

    def reload(self):
        now = datetime.utcnow()
        self.timestamp = (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)

    def to_datetime(self):
        return datetime(*self.timestamp, tzinfo=timezone.utc)

    def to_datetime_naive(self):
        return datetime(*self.timestamp, tzinfo=None)

    def to_unix_timestamp(self):
        return self.to_datetime().timestamp()

    def to_string(self):
        return self.to_datetime().strftime(self.timestamp_format)

    def to_string_iso8601(self):
        return self.to_datetime().strftime(FORMAT_ISO8601)

    @classmethod
    def from_datetime(cls, dt):
        return SystemTimestamp(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)

    @classmethod
    def from_string(cls, date_string, format=None):
        if format is None:
            format = cls.timestamp_format
        if date_string == '':
            return None
        else:
            dt = datetime.strptime(date_string, format)
            return cls.from_datetime(dt)

    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return self.timestamp == other.timestamp
