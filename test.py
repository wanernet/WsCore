# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf8')
from db.Model import *
from db.Field import *
from Kenel.JSON import *


class Ws_Member(Model):
    id = IntegerField(name='id', primary_key=True)
    account = StringField(name='account', column_type='varchar(50)')
    pwd = StringField(name='pwd', column_type='varchar(50)')
    email = StringField(name='email', column_type='varchar(200)')
    nickname = StringField(name='nickname', column_type='varchar(50)')
    create_time = TimestampField(name='create_time')
    last_time = TimestampField(name='last_time')
    display = BooleanField(name='display', default_value=False)


if __name__ == "__main__":
    # json = '{"account": "222", "display": 0, "nickname": "航收菜", "email": "4746445@qq.com", "pwd": "12322", "create_time": "2015-06-15 15:54:33", "last_time": "2015-06-15 23:27:31", "id": 2}'
    # u = Ws_Member.fromJSON(json)
    # print u
    # print u.account
    # print u.nickname
    # cur = int(time.time())
    # print cur
    # print time
    # u = Ws_Member(account='woshiw2', display=True, id=5)
    # print u.toJSON()
    # u.remove()
    # print u.hidden()
    # print u.save()
    # print u
    # ls = u.query(field='account,email')
    # for l in ls:
    # print l
    # u.id = u.insert()
    # print u
    # user = Ws_Member()
    # user.account
    result = Ws_Member.first_pk(2)
    # print result.toXML()
    # result.account
    # print result
    # print JSON.toJSON(result)
    # print result
    # print result.toJSON()
    # result.account = 'woshiw'
    # result.save()

    # u = ws_member(account='Michael')
    # result = ws_member.first(1)
    # print result
    # u.save()
    # ls = ws_member.query()
    # for l in ls:
    # print l.account
    # print ls