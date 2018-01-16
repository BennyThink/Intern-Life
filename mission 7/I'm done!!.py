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


def get_ip_mac_hn_index():
    se = []
    se2 = []
    for three in arp_info:
        for ip_mac_index in three.get('arp_list'):
            se.append(ip_mac_index)
            se2.append(three.get('hostname'))
    return se, se2


if __name__ == '__main__':
    s = []
    for three in arp_info:
        for ip_mac_index in three.get('arp_list'):
            s.append(ip_mac_index[0])
    print len(s)
    print len(set(s))
