#!/usr/bin/python
# -*- encoding:utf8 -*-

"""封装的mysql基类
@version:0.0.1
@author:waner(ShouCai Zhang)
@time:2015/06/03
"""
version = "0.0.1"

import sys

reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb


class MySQLHelper(object):
    def __init__(self, db_host, db_user, db_password, db_name):
        self._host = db_host
        self._user = db_user
        self._password = db_password
        self._db = db_name
        self.last_id = 0
        self.conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name, charset='utf8')
        if self.conn:
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def __del__(self):
        if self.conn:
            self.conn.commit()
            try:
                if type(self.cursor) == 'object':
                    self.cursor.close()
                if type(self.conn) == 'object':
                    self.conn.close()
            except MySQLdb.Error, e:
                print 'MYSQL close error: %s' % e.args[1]

    def __exit__(self):
        """ 注销对象时触发 关闭游标及数据库连接
        :return: 无
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def close(self):
        """ 关闭游标和数据库连接
        :return:无
        """
        self.__del__()

    def rollback(self):
        """ 事务回滚操作
        :return: 无
        """
        self.conn.rollback()

    def commit(self):
        """ 事务提交
        :return: 无
        """
        self.conn.commit()

    def __query(self, sql_text, args):
        """ SQL查询核心
        :param sql_text: 查询字符串，如：select * from member where account=%s and pwd=%s
        :param args: 查询条件值，如：('waner','123')
        :return: 返回 self.cursor.execute 或 None
        """
        if not sql_text:
            return None
        try:
            self.cursor.execute("SET NAMES utf8")
            if args:
                return self.cursor.execute(sql_text, args)
            else:
                return self.cursor.execute(sql_text)

        except MySQLdb.Error, e:
            print "mysql errcode:%s,message:%s" % (e.args[0], e.args[1])
            if args:
                print "sql error:%s,args:%s" % (sql_text, args)
            else:
                print "sql error:%s" % sql_text

        return None

    def execute(self, sql_text, args):
        """ 执行SQL语句
        :param sql_text: SQL字符串，如：update member set account=%s,pwd=%s where id=%s
        :param args: 值 或 条件值，如：('waner','123', 5)
        :return: 返回受影响的行数
        """
        result = self.__query(sql_text, args)
        if result is None:
            return None
        self.commit()
        return result

    def query(self, sql_text, args=None):
        """ 查询返回所有记录集
        :param sql_text: 查询字符串，如：select * from member where account=%s and pwd=%s
        :param args: 查询条件值，如：('waner','123')
        :return: 返回所有记录集 self.cursor.fetchall() 或 None
        """
        if not self.__query(sql_text, args):
            return None
        return self.cursor.fetchall()

    def first(self, sql_text, args=None):
        """ 查询返回单个记录
        :param sql_text: 查询字符串，如：select * from member where account=%s and pwd=%s
        :param args: 查询条件值，如：('waner','123')
        :return: 返回单个记录集 self.cursor.fetchone() 或 None
        """
        if not self.__query(sql_text, args):
            return None
        return self.cursor.fetchone()

    def rowcount(self):
        """ 返回记录数量
        :return: 返回 self.cursor.rowcount
        """
        return self.cursor.rowcount

    def insert(self, sql_text, args):
        """ 插入数据返回主键
        :param sql_text: 插入字符串，如：insert into member (account,pwd) values (%s,%s)
        :param args: 插入值，如：('waner','123')
        :return: 返回新增主键值 self.conn.insert_id()
        """
        self.cursor.execute("SET NAMES utf8")
        if args:
            self.cursor.execute(sql_text, args)
        else:
            self.cursor.execute(sql_text)

        self.last_id = self.conn.insert_id()
        self.commit()
        return self.last_id


if __name__ == "__main__":
    pass
