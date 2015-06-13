#!/usr/bin/python
# -*- encoding:utf8 -*-

"""封装的mysql基类
@version:1.0
@author:waner
@time:2015/06/03
"""
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb as mdb


class MySQLHelper(object):
    def __init__(self, db_host, db_user, db_password, db_name):
        self._host = db_host
        self._user = db_user
        self._password = db_password
        self._db = db_name
        self.conn = mdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name, charset='utf8')
        if self.conn:
            self.cursor = self.conn.cursor(mdb.cursors.DictCursor)

    def __del__(self):
        if self.conn:
            self.conn.commit()
            try:
                if type(self.cursor) == 'object':
                    self.cursor.close()
                if type(self.conn) == 'object':
                    self.conn.close()
            except mdb.Error, e:
                print 'MYSQL close error: %s' % e.args[1]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    # 关闭游标和数据库连接
    def close(self):
        self.__del__()

    # 事务回滚操作
    def rollback(self):
        self.conn.rollback()

    # 事务提交
    def commit(self):
        self.conn.commit()

    # 查询核心
    def __query(self, sql_text, **args):
        if not sql_text:
            return None
        try:
            self.cursor.execute("SET NAMES utf8")
            if args:
                return self.cursor.execute(sql_text)
            else:
                return self.cursor.execute(sql_text, **args)
        except mdb.Error, e:
            print "sql error:%s" % sql_text

        return None

    # 查询返回所有记录集
    def query(self, sql_text, **args):
        if not self.__query(sql_text, **args):
            return None
        return self.cursor.fetchall()

    # 查询返回单个记录
    def first(self, sql_text, **args):
        if not self.__query(sql_text, **args):
            return None
        return self.cursor.fetchone()

    # 返回记录数量
    def rowcount(self):
        return self.cursor.rowcount

    # 插入数据返回主键
    def insert(self, sql_text, **args):
        if not self.__query(sql_text, **args):
            return None
        self.commit()
        return self.conn.insert_id()

    # 更新记录
    def update(self, sql_text, **args):
        if not self.__query(sql_text, **args):
            return None
        self.commit()


if __name__ == "__main__":
    sql = MySQLHelper(db_host='127.0.0.1', db_user='root', db_password='wanersoft', db_name='novel_v11')
    names = u'张寿财3'
    str2 = "insert into ws_member(account) VALUE ('%s')" % names
    result = sql.insert(str2)
    print result

    row = sql.query('select * from ws_member')
    for r in row:
        print str(r[0]) + r[1]

