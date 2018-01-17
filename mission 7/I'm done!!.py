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


def get_ip_mac():
    ip_mac = []
    for i in arp_info:
        for j in i.get('arp_list'):
            ip_mac.append(tuple(j))
    return ip_mac


def hostname_ifname(mac):
    info = []
    for hn in mac_info:
        for vlan in hn.get('mac_dict'):
            for i in hn.get('mac_dict').get(vlan, [mac, 'N/A']):
                if i[0] == mac:
                    info.append((vlan, hn.get('hostname'), i[1], i[0]))
    return info


def get_desc(hn, ifname):
    for i in basic_info:
        if i.get('hostname') == hn:
            for j in i.get('if_index'):
                if i.get('if_index').get(j) == ifname:
                    return i.get('if_desc').get(j)


if __name__ == '__main__':
    x = get_ip_mac()

    for i in x:
        y = hostname_ifname(i[1])
        for ii in y:
            get_desc(ii[1], ii[2])
