#!/usr/bin/env python
# coding: utf-8


from datetime import datetime

from base.base import JobBase


class Fruit(JobBase):
    """
    Fruit-time reminder
    """
    cron = "50 7 * * 1-5"

    def run(self, args):
        title = "[%s] 生产环境上线通知" % datetime.now().strftime("%Y-%m-%d")
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
                                    "text": "吃水果啦啦啦啦啦啦啦， 吃水果有助于身心健康～ "
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