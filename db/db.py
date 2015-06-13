#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

import MySQLHelper


class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        """

        :rtype : object
        """
        super(StringField, self).__init__(name, ddl, primary_key, default)


class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super(BooleanField, self).__init__(name, 'boolean', False, default)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super(IntegerField, self).__init__(name, 'bigint', primary_key, default)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super(FloatField, self).__init__(name, 'real', primary_key, default)


class TextField(Field):
    def __init__(self, name=None, default=None):
        super(TextField, self).__init__(name, 'text', False, default)


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name == 'Model':
            return type.__new__(mcs, name, bases, attrs)

        table_name = attrs.get('__table__', None) or name
        print ('found model: %s (table: %s)' % (name, table_name))
        mappings = dict()
        fields = []
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                print ('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primary_key:
                        raise StandardError('Duplicate primary key for field: %s' % k)
                    primary_key = k
                else:
                    fields.append(k)
        if not primary_key:
            raise StandardError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primary_key  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        return type.__new__(mcs, name, bases, attrs)


class Model(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                #logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.iteritems():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))
        sql = MySQLHelper.MySQLHelper(db_host='127.0.0.1', db_user='root', db_password='wanersoft', db_name='novel_v11')
        result = sql.insert(sql % str(args))
        print result

    @classmethod
    def query(cls):
        sql = MySQLHelper.MySQLHelper(db_host='127.0.0.1', db_user='root', db_password='wanersoft', db_name='novel_v11')
        sql_str = 'select * from %s' % cls.__table__
        print sql_str
        d = sql.query(sql_str)
        # for name in d:
        #     print name
        print d
        #return d
        return [cls(**r) for r in d] if d else None

    @classmethod
    def first(cls, pk):
        sql = MySQLHelper.MySQLHelper(db_host='127.0.0.1', db_user='root', db_password='wanersoft', db_name='novel_v11')
        sql_str = 'select account,nickname from %s where %s=%s' % (cls.__table__, cls.__primary_key__, pk)
        print sql_str
        d = sql.first(sql_str)
        # for name in d:
        #     print name
        # print d
        #return d
        return cls(**d) if d else None


class ws_member(Model):
    id = IntegerField(name='id', primary_key=True)
    account = StringField(name='account')
    nickname = StringField(name='nickname')


if __name__ == "__main__":
    #u = ws_member(account='Michael')
    # result = ws_member.first(1)
    # print result
    # u.save()
    ls = ws_member.query()
    for l in ls:
        print l.account
    #print ls