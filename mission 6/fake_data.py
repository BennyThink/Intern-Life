#!/usr/bin/python
# coding:utf-8

# Intern-Life - fake_data.py
# 2017/12/15 14:57
# 

__author__ = 'Benny <benny@bennythink.com>'

import mysql.connector
import random



# cur.execute('')
# print cur.fetchall()
# 7 fieles
def g():
    field = ''
    for i in range(random.randint(1, 10)):
        field = field + chr(random.randint(48, 127))
    return field


if __name__ == '__main__':
    # cur.execute('insert into test VALUES (%s,%s,%s,%s,%s,%s,%s)')
    con = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='front')
    cur = con.cursor()

    for i in range(10):
        s = 'insert into test VALUES ("%s","%s","%s","%s","%s","%s","%s")' % (g(), g(), g(), g(), g(), g(), g(),)

        cur.execute(s)
    con.commit()
    con.close()
