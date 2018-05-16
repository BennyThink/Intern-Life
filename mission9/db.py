#!/usr/bin/python
# coding:utf-8

# Intern-Life - db.py
# 2018/4/24 12:50
# 

__author__ = 'Benny <benny@bennythink.com>'

import pymysql
import pymongo

ERROR = {
    1064: '数据库名名不合法',
    2003: '连接被拒绝，MySQL可能未开启或端口号错误',
    1045: '访问被拒绝，错误的用户名或密码',
    1049: '未知数据库，数据库不存在'}


class MySQLAPI:
    def __init__(self, host, port, user, password, database):
        try:
            self.con = pymysql.connect(host=host, port=port, user=user, password=password)
            self.cur = self.con.cursor()
            self.cur.execute('USE %s' % database)
            self.err_code = '0'
            self.err_msg = '添加成功'
        except Exception as e:
            self.err_code = e.args[0]
            self.err_msg = ERROR.get(e.args[0], e.args[1])

    def __del__(self):
        # TODO: Pythonic?
        try:
            self.cur.close()
            self.con.close()
        except AttributeError:
            pass

    def query(self, sql, param=None):
        self.cur.execute(sql, param)
        return self.cur.fetchall()


class MongoAPI:
    def __init__(self, host, port, user, password, database, auth):
        if not auth:
            auth = 'SCRAM-SHA-1'
        try:
            if user and password:
                self.mongo_client = pymongo.MongoClient(host=host, port=port, username=user, password=password,
                                                        authMechanism=auth, serverSelectionTimeoutMS=2)
            else:
                self.mongo_client = pymongo.MongoClient(host=host, port=port, serverSelectionTimeoutMS=2)
            # TODO：暂时这样
            # self.mongo_client.admin.command('ismaster')
            self.mongo_client.database_names()
            self.db = self.mongo_client[database]
            self.err_code = '0'
            self.err_msg = '添加成功'
        except Exception as e:
            self.err_code = '1'
            self.err_msg = e.args

    def __del__(self):
        try:
            self.mongo_client.close()
        except AttributeError:
            pass
