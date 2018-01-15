#!/usr/bin/python
# coding:utf-8

# Intern-Life - I'm done!!.py
# 2018/1/15 13:17
# 

__author__ = 'Benny <benny@bennythink.com>'

import json


def read_3_json():
    with open('arp_info.json') as f:
        f1 = json.load(f)
    with open('mac_info.json') as f:
        f2 = json.load(f)
    with open('basic_info.json') as f:
        f3 = json.load(f)

    return f1[0].get('data'), f2[0].get('data'), f3[0].get('data')


arp_info, mac_info, basic_info = read_3_json()
