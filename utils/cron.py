#!/usr/bin/env python3
# coding: utf-8


from datetime import datetime


def second_in_day(h, m, s) -> int:
    """
    Convert time to seconds in day
    """
    return h * 3600 + m * 60 + s

def near(hour, minute=0, second=0, diff=120) -> bool:
    """
    Check if time is near now
    """
    now = datetime.now()
    ns = second_in_day(now.hour, now.minute, now.second)
    ts = second_in_day(hour, minute, second)

    return abs(ns - ts) < diff


CRON_MINUTE = 1
CRON_HOUR = 2
CRON_DAY_OF_MONTH = 3
CRON_MONTH = 4
CRON_DAY_OF_WEEK = 5

VALUE_BASE = {
    CRON_MINUTE: list(range(0, 60)),
    CRON_HOUR: list(range(0, 24)),
    CRON_DAY_OF_MONTH: list(range(1, 32)),
    CRON_MONTH: list(range(1, 13)),
    CRON_DAY_OF_WEEK: list(range(0, 7))
}


MONTH_MAP = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}

WEEKDAY_MAP = {
    "SUN": 0,
    "MON": 1,
    "TUE": 2,
    "WED": 3,
    "THU": 4,
    "FRI": 5,
    "SAT": 6,
}


class CronValue(object):
    def __init__(self, values):
        self.values = set(values)
    
    def match(self, t):
        return t in self.values


def any_value(field):
    return list(VALUE_BASE[field])


def step_value(field, base, step):
    base = VALUE_BASE[field]
    for i in range(0, len(base), step):
        yield base[i]


def range_value(field, start, end):
    base = VALUE_BASE[field]
    for x in base:
        if start <= x <= end:
            yield x


def separated_value(field, values):
    base = set(VALUE_BASE[field])
    for x in values:
        if x in base:
            yield x


def cron_parse_value(field, text) -> CronValue:
    values = []
    if "/" in text:
        parts = text.split("/", 1)
        step = int(parts[1])
        values = step_value(field, parts[0], step)

    elif "-" in text:
        parts = text.split("-", 1)
        start = int(parts[0])
        end = int(parts[1])
        values = range_value(field, start, end)

    elif "," in text:
        parts = text.split(",")
        values = separated_value(field, map(int, parts))

    elif "*" == text:
        values = any_value(field)

    else:
        values = [int(text)]

    return CronValue(values)


class CronItem(object):
    """
    Crontab item
    """
    def __init__(self, minute="*", hour="*", dom="*", month="*", dow="*") -> None:
        self.minute = cron_parse_value(CRON_MINUTE, minute)
        self.hour = cron_parse_value(CRON_HOUR, hour)
        self.dom = cron_parse_value(CRON_DAY_OF_MONTH, dom)
        self.month = cron_parse_value(CRON_MONTH, month)
        self.dow = cron_parse_value(CRON_DAY_OF_WEEK, dow)

    def match(self, t: datetime = None) -> bool:
        if t is None:
            t = datetime.now()

        matched_fields = [
            self.minute.match(t.minute),
            self.hour.match(t.hour),
            self.dom.match(t.day),
            self.month.match(t.month),
            self.dow.match((t.weekday() + 1) % 7)
        ]

        print(matched_fields)
        return all(matched_fields)


def cron_parse(text) -> CronItem:
    parts = text.split()
    if len(parts) != 5:
        raise ValueError("Invalid cron format")

    return CronItem(*parts)
