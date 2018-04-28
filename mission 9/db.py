#!/usr/bin/python
# coding:utf-8

# Intern-Life - db.py
# 2018/4/24 12:50
# 

__author__ = 'Benny <benny@bennythink.com>'

import mysql.connector
import pymongo


class MySQLAPI:
    def __init__(self, host, port, user, password, database):
        self.con = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        self.cur = self.con.cursor()

    def __del__(self):
        self.con.close()

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
