#!/usr/bin/python
# coding:utf-8

# Intern-Life - mem_test.py
# 2017/11/2 9:20
# 

__author__ = 'Benny <benny@bennythink.com>'

import sys
import time

s = []

while 1:
    if sys.getsizeof(s) / 1024 / 1024 > 100:
        break
    else:
        s.append(' ')

time.sleep(30)
