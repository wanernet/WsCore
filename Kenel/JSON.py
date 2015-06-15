#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Waner <wanernet@qq.com>'
__all__ = ["JSON", "JSONEncoder"]

import json
from datetime import date, datetime


def JSONEncoder(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    else:
        return json.JSONEncoder.default(obj)
        # raise TypeError('%r is not JSON serializable' % obj)


class JSON(object):
    def __init__(self):
        pass

    @classmethod
    def toJSON(cls, s, indent=None):
        return json.dumps(s, default=JSONEncoder, indent=indent)

    @classmethod
    def formJSON(cls, s):
        return json.loads(s, encoding="utf-8")