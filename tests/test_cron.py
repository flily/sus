#!/usr/bin/env python3
# coding: utf-8

import unittest
from datetime import datetime

import utils.cron as cron


class TestCronValue(unittest.TestCase):
    def test_cron_any_value(self):
        got = cron.any_value(cron.CRON_MINUTE)
        exp = range(0, 60)
        self.assertEqual(list(got), list(exp))

        got = cron.any_value(cron.CRON_HOUR)
        exp = range(0, 24)
        self.assertEqual(list(got), list(exp))

        got = cron.any_value(cron.CRON_DAY_OF_MONTH)
        exp = range(1, 32)
        self.assertEqual(list(got), list(exp))

        got = cron.any_value(cron.CRON_MONTH)
        exp = range(1, 13)
        self.assertEqual(list(got), list(exp))

        got = cron.any_value(cron.CRON_DAY_OF_WEEK)
        exp = range(0, 7)
        self.assertEqual(list(got), list(exp))

    def test_cron_step_value(self):
        got = cron.step_value(cron.CRON_MINUTE, 0, 6)
        exp = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54]
        self.assertEqual(list(got), list(exp))

        got = cron.step_value(cron.CRON_HOUR, 0, 3)
        exp = [0, 3, 6, 9, 12, 15, 18, 21]
        self.assertEqual(list(got), list(exp))

        got = cron.step_value(cron.CRON_DAY_OF_MONTH, 0, 3)
        exp = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31]
        self.assertEqual(list(got), list(exp))

        got = cron.step_value(cron.CRON_MONTH, 0, 3)
        exp = [1, 4, 7, 10]
        self.assertEqual(list(got), list(exp))

        got = cron.step_value(cron.CRON_DAY_OF_WEEK, 0, 3)
        exp = [0, 3, 6]
        self.assertEqual(list(got), list(exp))

    def test_cron_range_value(self):
        got = cron.range_value(cron.CRON_MINUTE, 3, 6)
        exp = [3, 4, 5, 6]
        self.assertEqual(list(got), list(exp))

        got = cron.range_value(cron.CRON_HOUR, 3, 6)
        exp = [3, 4, 5, 6]
        self.assertEqual(list(got), list(exp))

        got = cron.range_value(cron.CRON_DAY_OF_MONTH, 3, 6)
        exp = [3, 4, 5, 6]
        self.assertEqual(list(got), list(exp))

        got = cron.range_value(cron.CRON_MONTH, 3, 6)
        exp = [3, 4, 5, 6]
        self.assertEqual(list(got), list(exp))

        got = cron.range_value(cron.CRON_DAY_OF_WEEK, 3, 6)
        exp = [3, 4, 5, 6]
        self.assertEqual(list(got), list(exp))


    def test_cron_separated_value(self):
        got = cron.separated_value(cron.CRON_MINUTE, [3, 4, 5, 6])
        exp = [3, 4, 5, 6]
        self.assertEqual(list(got), list(exp))

        got = cron.separated_value(cron.CRON_HOUR, [3, 4, 5, 6])
        exp = [3, 4, 5, 6]
        self.assertEqual(list(got), list(exp))
        
        got = cron.separated_value(cron.CRON_DAY_OF_MONTH, [3, 4, 5, 6])
        exp = [3, 4, 5, 6]
        self.assertEqual(list(got), list(exp))
        
        got = cron.separated_value(cron.CRON_MONTH, [3, 4, 5, 6])
        exp = [3, 4, 5, 6]
        self.assertEqual(list(got), list(exp))
        
        got = cron.separated_value(cron.CRON_DAY_OF_WEEK, [3, 4, 5, 6])
        exp = [3, 4, 5, 6]
        self.assertEqual(list(got), list(exp))


class TestCronItem(unittest.TestCase):
    def test_cron_item_for_all_any(self):
        item = cron.cron_parse("* * * * *")
        now = datetime.now()
        self.assertTrue(item.match(now))

    def test_cron_item_for_fixed_minute(self):
        item = cron.cron_parse("42 * * * *")

        for h in range(0, 24):
            t = datetime(year=2017, month=1, day=1, hour=h, minute=42)
            self.assertTrue(item.match(t))

        for h in range(0, 24):
            t = datetime(year=2017, month=1, day=1, hour=h, minute=41)
            self.assertFalse(item.match(t))

    def test_cron_item_for_weekdays(self):
        cases = [
            (datetime(year=2022, month=8, day=7, hour=6, minute=49), False),
            (datetime(year=2022, month=8, day=7, hour=6, minute=50), False),
            (datetime(year=2022, month=8, day=7, hour=6, minute=51), False),
            (datetime(year=2022, month=8, day=8, hour=6, minute=49), False),
            (datetime(year=2022, month=8, day=8, hour=6, minute=50), True),
            (datetime(year=2022, month=8, day=8, hour=6, minute=51), False),
            (datetime(year=2022, month=8, day=9, hour=6, minute=49), False),
            (datetime(year=2022, month=8, day=9, hour=6, minute=50), True),
            (datetime(year=2022, month=8, day=9, hour=6, minute=51), False),
            (datetime(year=2022, month=8, day=10, hour=6, minute=49), False),
            (datetime(year=2022, month=8, day=10, hour=6, minute=50), True),
            (datetime(year=2022, month=8, day=10, hour=6, minute=51), False),
            (datetime(year=2022, month=8, day=11, hour=6, minute=49), False),
            (datetime(year=2022, month=8, day=11, hour=6, minute=50), True),
            (datetime(year=2022, month=8, day=11, hour=6, minute=51), False),
            (datetime(year=2022, month=8, day=12, hour=6, minute=49), False),
            (datetime(year=2022, month=8, day=12, hour=6, minute=50), True),
            (datetime(year=2022, month=8, day=12, hour=6, minute=51), False),
            (datetime(year=2022, month=8, day=13, hour=6, minute=49), False),
            (datetime(year=2022, month=8, day=13, hour=6, minute=50), False),
            (datetime(year=2022, month=8, day=13, hour=6, minute=51), False),
        ]

        item = cron.cron_parse("50 6 * * 1-5")
        for t, exp in cases:
            self.assertEqual(item.match(t), exp, t)

        item = cron.cron_parse("50 6 * * 1,2,3,4,5")
        for t, exp in cases:
            self.assertEqual(item.match(t), exp, t)
