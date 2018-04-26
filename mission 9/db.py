#!/usr/bin/python
# coding:utf-8

# Intern-Life - db.py
# 2018/4/24 12:50
# 

__author__ = 'Benny <benny@bennythink.com>'

import mysql.connector


class DatabaseAPI:
    def __init__(self, host, user, password, database):
        self.con = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cur = self.con.cursor()

    def __del__(self):
        self.con.close()

    def query(self, sql, param=None):
        self.cur.execute(sql, param)
        return self.cur.fetchall()
