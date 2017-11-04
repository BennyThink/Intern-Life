#!/usr/bin/python
# coding:utf-8

# Intern-Life - test.py
# 2017/11/3 15:07
# 

__author__ = 'Benny <benny@bennythink.com>'

# dic test
import mysql.connector

con = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='san')

cur = con.cursor()
cur.execute('show  COLUMNS from %s' % 'san_device')

col_data = cur.fetchall()
col_field = [i[0] for i in col_data]

print col_field

cur.execute('select * from %s'%'san_device')
data = cur.fetchmany(2)
dic = dict(zip(col_field, data[0]))
dic.update(_index='san', _type='san_device')

SIZE = 20

while True:
    data = cur.fetchmany(SIZE)
    if data:
        bulk_dic = []
        for i in range(len(data)):
            es_dic = dict(zip(col_field, data[i]))
            es_dic.update(_index='san', _type='san_device')
            bulk_dic.append(es_dic)
    else:
        break

print bulk_dic