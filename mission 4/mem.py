#!/usr/bin/python
# coding:utf-8

# Intern-Life - mem.py
# 2017/11/16 9:25
# Python 2 ONLY.
# 2017-11-17 15:03:01
# This time it seems right...

__author__ = 'Benny <benny@bennythink.com>'

import sys
import mysql.connector
import time


def recursive(var):
    """
    calculate variables' memory consumption
    :param var: str,float,unicode,int,list and tuple only.
    :return: size in bytes.
    """

    if isinstance(var, (int, float, unicode, str)):
        return sys.getsizeof(var)

    else:
        size = sys.getsizeof(var)
        for i in var:
            size += recursive(i)
        return size


def test():
    """
    get big result set.
    :return: result set in the form of [(...), (...)]
    """
    con = mysql.connector.connect(user='root', password='root', database='info')
    cur = con.cursor()
    cur.execute('select * from san_device')
    data = cur.fetchmany(50000)
    return data


if __name__ == '__main__':
    s = [(1, 2, 3), (1, 2)]
    # Notes:
    # 50000     100000      200000
    # 49.9-41   95.1-84     185.9-169
    print recursive(test()) / 1024.0 / 1024.0
    time.sleep(100)
