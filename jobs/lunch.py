#!/usr/bin/env python
# coding: utf-8


from datetime import datetime

from base.base import JobBase


class Lunch(JobBase):
    """
    Lunch-time reminder
    """
    cron = "40 3 * * 1-5"

    def run(self, args):
        title = "[%s] 午饭时间通知" % datetime.now().strftime("%Y-%m-%d")
        m = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": "该吃午饭啦，吃饱了才能继续搬砖！"
                                },
                                {
                                    "tag": "a",
                                    "text": "调教bot点击这里",
                                    "href": "https://github.com/flily/sus"
                                }
                            ]
                        ]
                    }
                }
            }
        }

        r = self.send_message(m)
        if r is None:
            return

        print(r.json())
