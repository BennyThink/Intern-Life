#!/usr/bin/python
# coding:utf-8

# Intern-Life - mem.py
# 2017/11/16 9:25
# Python 2 ONLY.

__author__ = 'Benny <benny@bennythink.com>'

import sys
import mysql.connector
import time

SIZE = 0


def recursive(var):

    global SIZE
    if isinstance(var, str) or isinstance(var, unicode) or isinstance(var, int) or isinstance(var, float):
        SIZE += sys.getsizeof(var)
    elif isinstance(var, list) or isinstance(var, tuple):
        for i in var:
            if isinstance(i, list) or isinstance(i, tuple):
                recursive(i)
            elif isinstance(i, str) or isinstance(i, unicode) or isinstance(i, int) or isinstance(i, float):
                # Strange...?
                SIZE += sys.getsizeof(var)
                break
    elif isinstance(var, dict):
        pass
    else:
        SIZE += sys.getsizeof(var)
        recursive(var)


def test():
    con = mysql.connector.connect(user='root', password='root', database='san')
    cur = con.cursor()
    cur.execute('select * from san_device')
    data = cur.fetchmany(2)
    recursive(data)
    print SIZE / 1024.0 / 1024.0
    time.sleep(100)


if __name__ == '__main__':
    test()
