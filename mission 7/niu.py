#!/usr/bin/python
# coding:utf-8

# Intern-Life - new.py
# 2018/1/14 19:45
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


def get_ip_mac_index_gateway():
    ip_list = []
    mac_list = []
    index_list = []
    gateway_list = []

    for ip_mac_id in arp_info:
        for ip in ip_mac_id.get('arp_list'):
            ip_list.append(ip[0])
            mac_list.append(ip[1])
            index_list.append(ip[2])
            gateway_list.append(ip_mac_id.get('hostname'))

    return ip_list, mac_list, index_list, gateway_list


def parse_vhi(mac):
    for hn in mac_info:
        # if hn.get('hostname') == gw:
        for vlan in hn.get('mac_dict'):
            for i in hn.get('mac_dict').get(vlan, [mac, 'N/A']):
                if i[0] == mac:
                    # return i[0], vlan, gw, i[1]
                    return vlan, hn.get('hostname'), i[1]


def get_vlan_hostname_interface(mac, gw):
    result = parse_vhi(mac)
    if result is None:
        return 'N/A', gw, 'N/A'
    else:
        return result


def get_desc(gw, index):
    for item in basic_info:
        if item.get('hostname') == gw:
            return item.get('if_desc').get(index)


def get_some():
    a, b, c, d = get_ip_mac_index_gateway()
    ip_list, m_list, index_list, gw_list = list(a), list(b), list(c), list(d)
    vlan_list = []
    hostname_list = []
    interface_list = []
    desc_list = []

    while len(b) > 0:
        res = get_vlan_hostname_interface(b[-1], d[-1])
        vlan_list.append(res[0])
        hostname_list.append(res[1])
        interface_list.append(res[2])
        res = get_desc(d[-1], c[-1])
        desc_list.append(res)
        # TODO: this is very slow, how about pop(-1), try deque or...?
        a.pop(-1)
        b.pop(-1)
        c.pop(-1)
        d.pop(-1)

    final = zip(ip_list, m_list, vlan_list, hostname_list, interface_list, index_list, desc_list)
    return final


def insert():
    res = get_some()
    print type(res)

    con = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='front')
    cur = con.cursor()
    cmd = 'INSERT INTO test3 VALUES (%s,%s,%s,%s,%s,%s,%s)'
    cur.execute("SET GLOBAL max_allowed_packet=1073741824")
    cur.execute('SET GLOBAL CONNECT_TIMEOUT = 600')
    cur.execute('SET SESSION NET_READ_TIMEOUT = 6000')

    cur.executemany(cmd, res)
    con.commit()
    con.close()


if __name__ == '__main__':
    insert()
