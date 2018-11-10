# -*- coding: utf-8 -*-
""" TestSystemTimestamp """
from datetime import datetime, timedelta, timezone

from xross_common.SystemLogger import SystemLogger
from xross_common.SystemTimestamp import SystemTimestamp, FORMAT_ISO8601
from xross_common.XrossTestBase import XrossTestBase

JST = timezone(timedelta(hours=+9), 'JST')


class TestSystemTimestamp(XrossTestBase):
    logger, test_handler = SystemLogger("TestSystemTimestamp").get_logger()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_default(self):
        ts = SystemTimestamp()
        print(datetime.now(JST).astimezone(tz=timezone.utc))
        print(ts.to_datetime())
        self.assertAlmostEqual(datetime.now(JST).astimezone(tz=timezone.utc), ts.to_datetime(), delta=timedelta(0, 1))

    def test_from_datetime(self):
        dt = datetime(2018, 2, 11, 8, 38, 0, 0, tzinfo=timezone.utc)
        ts = SystemTimestamp(2018, 2, 11, 8, 38, 0, 0)
        self.assertEqual(ts, SystemTimestamp.from_datetime(dt))

    def test_to_datetime(self):
        ts = SystemTimestamp(2018, 2, 11, 8, 38, 0, 0)
        self.assertEqual(datetime(2018, 2, 11, 8, 38, 0, 0, tzinfo=timezone.utc), ts.to_datetime())

    def test_to_string(self):
        ts = SystemTimestamp(2018, 2, 11, 8, 38, 0, 0)
        self.assertEqual("2018-02-11 08:38:00.000000", ts.to_string())

    def test_to_string_iso(self):
        ts = SystemTimestamp(2018, 2, 11, 8, 38, 0, 0)
        self.assertEqual("2018-02-11T08:38:00.000000Z", ts.to_string_iso8601())

    def test_from_string(self):
        self.assertEqual(SystemTimestamp(2018, 2, 11, 8, 38, 0, 0),
                         SystemTimestamp.from_string("2018-02-11 08:38:00.000000"))

    def test_from_string_iso(self):
        self.assertEqual(SystemTimestamp(2018, 2, 11, 8, 38, 0, 0),
                         SystemTimestamp.from_string("2018-02-11T08:38:00.000000Z", format=FORMAT_ISO8601))

    def test_to_unix_timestamp(self):
        ts = SystemTimestamp(2018, 2, 11, 8, 38, 0, 0)
        self.assertEqual(1518338280.0, ts.to_unix_timestamp())

    def test_to_string_tz(self):
        expiry_date = SystemTimestamp(2015, 1, 30, 15, 0, 0, 0).to_datetime()
        self.assertEqual(datetime(2015, 1, 30, 15, 0, 0, 0, tzinfo=timezone.utc), expiry_date)
