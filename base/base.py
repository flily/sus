#!/usr/bin/env python3
# coding: utf-8


import abc

import requests

from utils.cron import cron_parse

WEB_HOOK_URL_BASE = "https://open.feishu.cn/open-apis/bot/v2/hook/{0}"


class JobBase(object):
    """
    Job base class, implement to run auto FEISHU-bot jobs.
    """
    cron = "* * * * *"

    def __init__(self, web_hook_id) -> None:
        self.web_hook_id = web_hook_id
        self.dry_run = False

    def _get_web_hook_url(self) -> str:
        return WEB_HOOK_URL_BASE.format(self.web_hook_id)

    @abc.abstractmethod
    def run(self, args):
        pass

    def is_scheduled(self, now):
        item = cron_parse(self.cron)
        return item.match(now)

    def send_message(self, message):
        url = self._get_web_hook_url()
        if self.dry_run:
            print("POST %s" % url)
            print(message)
            return None

        else:
            response = requests.request("POST", url, json=message)
            return response

class JobException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return self.message
