#!/usr/bin/python
# coding:utf-8

# Intern-Life - massive_data_test.py
# 2017/11/2 9:35
# 

__author__ = 'Benny <benny@bennythink.com>'

import mysql.connector
import time
import sys

SIZE = 100000
con = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='san')


def test():
    cur = con.cursor()
    cur.execute('select * from san_device')

    while True:
        data = cur.fetchmany(10)

        if data:
            print data
        else:
            break


    con.close()


if __name__ == '__main__':
    test()

