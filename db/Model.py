#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')
from mysql.MySQLHelper import MySQLHelper
from ModelMetaclass import ModelMetaclass
from Kenel.JSON import JSON
from Kenel.XML import XML


class Model(dict):
    """ 实体继承基类
    """
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
                setattr(self, key, value)
        return value

    def insert(self):
        """ 实体数据插入数据库，注意：插入字段根据实体已赋值字段生成
        :return: 返回新增主键值
        """
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.iteritems():
            if v.name != self.__primary_key__:
                val = self.getValue(v.name)
                if val is not None:
                    fields.append(v.name)
                    params.append('?')
                    args.append(val)

        sql_str = 'INSERT INTO %s (%s) VALUES (%s);' % (self.__table__, ','.join(fields), ','.join(params))
        sql_str = sql_str.replace('?', '%s')
        args = tuple(args)
        sql = MySQLHelper(db_host='127.0.0.1', db_user='root', db_password='wanersoft', db_name='novel_v11')
        return sql.insert(sql_str, args)

    def save(self):
        """ 根据主键值 更新实体数据
        :return: 返回影响行数
        """
        fields = []
        args = []
        for k, v in self.__mappings__.iteritems():
            if v.name != self.__primary_key__:
                val = self.getValue(v.name)
                if val is not None:
                    fields.append(v.name)
                    args.append(val)

        sql_str = 'UPDATE `%s` SET %s WHERE `%s`=?;' % (self.__table__,
                                                        ', '.join(map(
                                                            lambda f: '`%s`=?' % (self.__mappings__.get(f).name or f),
                                                            fields)),
                                                        self.__primary_key__)
        sql_str = sql_str.replace('?', '%s')
        args.append(self.getValueOrDefault(self.__primary_key__))
        args = tuple(args)

        sql = MySQLHelper(db_host='127.0.0.1', db_user='root', db_password='wanersoft', db_name='novel_v11')
        return sql.execute(sql_str, args)

    def remove(self):
        """ 根据主键 删除记录
        :return: 返回受影响的行数
        """
        args = tuple([self.getValue(self.__primary_key__)])
        sql_str = 'DELETE FROM `%s` WHERE `%s`=?' % (self.__table__, self.__primary_key__)
        sql_str = sql_str.replace('?', '%s')
        sql = MySQLHelper(db_host='127.0.0.1', db_user='root', db_password='wanersoft', db_name='novel_v11')
        return sql.execute(sql_str, args)

    def hidden(self):
        """ 根据主键 屏蔽记录
        :return: 返回受影响的行数
        """
        args = tuple([self.getValue(self.__primary_key__)])
        sql_str = 'UPDATE `%s` SET display=0 WHERE `%s`=?' % (self.__table__, self.__primary_key__)
        sql_str = sql_str.replace('?', '%s')
        sql = MySQLHelper(db_host='127.0.0.1', db_user='root', db_password='wanersoft', db_name='novel_v11')
        return sql.execute(sql_str, args)

    @classmethod
    def execute(cls, sql_str, where=None, args=None):
        """ 执行SQL语句
        :param sql_str: delete from %s 或者 update %s set
        :param where: 条件，如：account=? and pwd=?
        :param args: 条件值，如：('waner','123')
        :return: 返回受影响的行数
        """
        sql_str = sql_str % cls.__table__
        if where:
            sql_str += ' where %s' % where

        sql_str = sql_str.replace('?', '%s')
        sql = MySQLHelper(db_host='127.0.0.1', db_user='root', db_password='wanersoft', db_name='novel_v11')
        return sql.execute(sql_str, args)

    @classmethod
    def get_sql_str(cls, top=0, field=None, where=None):
        """ 生成查询字符串
        :param top: top数量，如：10
        :param field: 读取字段，如：id,account,pwd
        :param where: 条件，如：account=? and pwd=?
        :return:
        """
        sql_str = 'select %s`%s`,%s from %s' % (('' if top == 0 else ('top %s ' % top)), cls.__primary_key__,
                                                ', '.join(cls.__fields__), cls.__table__)
        if field:
            sql_str = 'select %s%s from %s' % (('' if top == 0 else ('top %s ' % top)), field, cls.__table__)

        if where:
            sql_str += ' where %s' % where
        # print sql_str
        return sql_str.replace('?', '%s')

    @classmethod
    def query(cls, top=0, field=None, where=None, args=None):
        """ 多条件查询结果集
        :param top: top数量，如：10
        :param field: 读取字段，如：id,account,pwd
        :param where: 条件，如：account=? and pwd=?
        :param args: 条件值，如：('waner','123')
        :return: 返回实体记录集对象 或 None
        """
        sql = MySQLHelper(db_host='127.0.0.1', db_user='root', db_password='wanersoft', db_name='novel_v11')
        sql_str = cls.get_sql_str(top, field, where)
        rs = sql.query(sql_str, args)
        return [cls(**r) for r in rs] if rs else None

    @classmethod
    def first(cls, field=None, where=None, args=None):
        """ 多条件查找唯一记录
        :param field: 读取字段，如：id,account,pwd
        :param where: 条件，如：account=? and pwd=?
        :param args: 条件值，如：('waner','123')
        :return:返回单一记录实体对象 或 None
        """
        sql = MySQLHelper(db_host='127.0.0.1', db_user='root', db_password='wanersoft', db_name='novel_v11')
        sql_str = cls.get_sql_str(0, field, where)
        r = sql.first(sql_str, args)
        return cls(**r) if r else None

    @classmethod
    def first_pk(cls, pk, field=None):
        """ 根据主键查找唯一记录
        :param pk: 主键值，如：5
        :param field: 读取字段，如：id,account,pwd
        :return:返回单一记录实体对象 或 None
        """
        sql = MySQLHelper(db_host='127.0.0.1', db_user='root', db_password='wanersoft', db_name='novel_v11')
        sql_str = cls.get_sql_str(field=field, where=cls.__primary_key__ + '=?')
        # print sql_str
        r = sql.first(sql_str, pk)
        return cls(**r) if r else None

    def toJSON(self):
        """ 转换JSON格式
        :return:
        """
        return JSON.toJSON(self)

    @classmethod
    def fromJSON(cls, s):
        r = JSON.formJSON(s)
        return cls(**r) if r else None

    # def toXML(self):
    #     json = self.toJSON()
    #     return XML.toXML(json)
    #
    # @classmethod
    # def formXML(cls, xml):
    #     json = JSON.toJSON(XML.formXML(xml), indent=4)
    #     return cls.fromJSON(json)


if __name__ == "__main__":
    pass