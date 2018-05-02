#!/usr/bin/python
# coding:utf-8

# Intern-Life - db.py
# 2018/4/24 12:50
# 

__author__ = 'Benny <benny@bennythink.com>'

import pymysql
import pymongo

ERROR = {1007: 'ProgrammingError 表已存在',
         1064: ' ProgrammingError 表名不合法',
         2003: 'OperationalError 连接被拒绝',
         1045: 'OperationalError 访问拒绝，错误的用户名或密码'}


class MySQLAPI:
    def __init__(self, host, port, user, password, database):
        try:
            self.con = pymysql.connect(host=host, port=int(port), user=user, password=password)
            self.cur = self.con.cursor()
            self.cur.execute('CREATE DATABASE %s' % database)
            self.err_code = '0'
            self.err_msg = '添加成功'
        except Exception as e:
            self.err_code = e[0]
            self.err_msg = ERROR.get(e[0], e[1])

    # def __del__(self):
    #     self.con.close()

    def query(self, sql, param=None):
        self.cur.execute(sql, param)
        return self.cur.fetchall()


class MongoAPI:
    def __init__(self, host, port, user, password, database, auth):
        self.mongo_client = pymongo.MongoClient(host=host, port=port, username=user, password=password,
                                                authMechanism=auth)
        self.db = self.mongo_client[database]

    def __del__(self):
        self.mongo_client.close()

    def query(self, sql, param=None):
        self.cur.execute(sql, param)
        return self.cur.fetchall()
