#!/usr/bin/python
# coding:utf-8

# Intern-Life - new2.py
# 2018/1/15 10:53
# 

__author__ = 'Benny <benny@bennythink.com>'

import json
import mysql.connector


def read_3_json():
    with open('arp_info.json') as f:
        f1 = json.load(f)
    with open('mac_info.json') as f:
        f2 = json.load(f)
    with open('basic_info.json') as f:
        f3 = json.load(f)

    return f1[0].get('data'), f2[0].get('data'), f3[0].get('data')


arp_info, mac_info, basic_info = read_3_json()


def get_mac():
    mac_list = []
    interface_list = []
    vlan_list = []
    hostname_list = []
    for hn in mac_info:
        for vlan in hn.get('mac_dict'):
            for i in hn.get('mac_dict').get(vlan):
                mac_list.append(i[0])
                interface_list.append(i[1])
                vlan_list.append(vlan)
                hostname_list.append(hn.get('hostname'))

    return mac_list, interface_list, vlan_list, hostname_list


def get_ip_index(mac):
    for info in arp_info:
        for ip_index in info.get('arp_list'):
            if ip_index[1] == mac:
                return ip_index[0], ip_index[1], ip_index[2]


def get_desc(hostname, index):
    for b in basic_info:
        if b.get('hostname') == hostname:
            return b.get('if_desc').get('151192552')


if __name__ == '__main__':
    mac, inter, vlan, hostname = get_mac()
    print hostname[0]
    print get_ip_index(mac[0])
