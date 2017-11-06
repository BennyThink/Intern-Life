#!/usr/bin/python
# coding:utf-8

# Intern-Life - mem_test.py
# 2017/11/2 9:20
# 

__author__ = 'Benny <benny@bennythink.com>'

import sys
import time
import mysql.connector

con = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='info')
cur = con.cursor()
cur.execute('select * from san_device')
data = cur.fetchmany(50000)
print (sys.getsizeof(data)+len(data) * sys.getsizeof(data[0]) )/ float(1024)/1024

#print sys.getsizeof(data[0])
time.sleep(30)