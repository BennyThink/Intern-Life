#!/usr/bin/python
# coding:utf-8

# Intern-Life - redo.py
# 2018/1/18 13:52
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


def generate_dict():
    basic_dict = {}
    for hn in basic_info:
        basic_dict.setdefault(hn.get('hostname'), {})
        for index in hn.get('if_index'):
            if index in hn.get('if_desc'):
                # TODO tuple unpacking
                basic_dict[hn.get('hostname')].update(
                    {hn.get('if_index').get(index).lower(): [index, hn.get('if_desc').get(index)]})

    # print basic_dict['JD70SW15-B1-VDC2']['Port-channel200'.lower()]
    # TODO  split it
    arp_dict = {}
    for arp_list in arp_info:
        for i in arp_list.get('arp_list'):
            ip, mac, _ = i
            arp_dict.setdefault(i[1], [])
            arp_dict[mac].append([arp_list.get('hostname'), ip])
    # basic_dict[hostname][inftc_name] = intfc_desc
    # arp_dict[mac_addr] = [[gateway, ip], []]

    return arp_dict, basic_dict


def run():
    arp_dict, basic_dict = generate_dict()
    # print arp_dict
    # print basic_dict
    # print arp_dict['00:26:98:0a:5f:43']

    write2db, used_mac = [], []
    for hn in mac_info:
        for vlan in hn['mac_dict']:
            for item in hn['mac_dict'][vlan]:
                # TODO:??
                # if len(item)!=2:
                #     print item
                mac_addr, inftc_name = item[0], item[-1]
                used_mac.append(mac_addr)
                # TODO: CASE
                intfc_desc = basic_dict.get(hn['hostname'], {}).get(inftc_name.lower(), '')
                # ???
                gateway_info = arp_dict.get(mac_addr, [])

                for ip_gw in gateway_info:
                    write2db.append((ip_gw[-1], mac_addr, vlan, hn['hostname'], inftc_name, intfc_desc, ip_gw[0]))

    for gateway in arp_info:
        for item in gateway.get('arp_list'):
            ip, mac_addr, _ = item
            if not mac_addr in used_mac:
                write2db.append((ip, mac_addr, '', '', '', '', gateway.get('hostname')))

    print len(write2db)

    # con = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='front')
    # cur = con.cursor()
    # cmd = 'INSERT INTO test2 VALUES (NULL ,%s,%s,%s,%s,%s,%s,%s)'
    # cur.execute("SET GLOBAL max_allowed_packet=1073741824")
    # cur.execute('SET GLOBAL CONNECT_TIMEOUT = 600')
    # cur.execute('SET SESSION NET_READ_TIMEOUT = 6000')
    #
    # cur.executemany(cmd, write2db)
    # con.commit()
    # con.close()


if __name__ == '__main__':
    arp_dict, basic_dict = generate_dict()
    # print arp_dict
    print basic_dict['JD70SW31-B1-VDC2'].get('Ethernet7/10'.lower())
    # print arp_dict['00:26:98:0a:5f:43']
