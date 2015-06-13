#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Field(object):
    def __init__(self, name, column_type, primary_key, default_value):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default_value = default_value

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default_value=None, column_type='varchar(50)'):
        super(StringField, self).__init__(name, column_type, primary_key, default_value)


class BooleanField(Field):
    def __init__(self, name=None, default_value=False):
        super(BooleanField, self).__init__(name, 'boolean', False, default_value)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default_value=0):
        super(IntegerField, self).__init__(name, 'int', primary_key, default_value)


class BigIntegerField(Field):
    def __init__(self, name=None, primary_key=False, default_value=0):
        super(BigIntegerField, self).__init__(name, 'bigint', primary_key, default_value)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default_value=0.0):
        super(FloatField, self).__init__(name, 'real', primary_key, default_value)


class TextField(Field):
    def __init__(self, name=None, default_value=None):
        super(TextField, self).__init__(name, 'text', False, default_value)


class TimestampField(Field):
    def __init__(self, name=None, default_value=None):
        super(TimestampField, self).__init__(name, 'timestamp', False, default_value)
