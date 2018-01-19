#!/usr/bin/python
# coding:utf-8

# Intern-Life - redo.py
# 2018/1/18 13:52
# for more information please check the two txt files.

__author__ = 'Benny <benny@bennythink.com>'

import json

import mysql.connector
from openpyxl import Workbook


def generate_basic_dict():
    """
    generate a dict according to basic_info.json, provide searching for interface description
    :return: a dict like {'JD70SW24-B1-VDC2': {'ethernet4/11': 'this is description'}}
    """
    with open('basic_info.json') as f:
        basic_info = json.load(f)[0].get('data')

    basic_dict = {}
    for hn in basic_info:
        basic_dict.setdefault(hn.get('hostname'), {})
        for index in hn.get('if_index'):
            if index in hn.get('if_desc'):
                # TODO tuple unpacking
                basic_dict[hn.get('hostname')].update(
                    {hn.get('if_index').get(index).lower(): hn.get('if_desc').get(index)})

    return basic_dict


def parse_arp_mac():
    with open('mac_info.json') as f:
        mac_info = json.load(f)[0].get('data')
    with open('arp_info.json') as f:
        arp_info = json.load(f)[0].get('data')

    basic_dict = generate_basic_dict()
    arp_dict = {}
    # generate arp_dict, the key is mac address, value is hostname & IP in a list.
    for arp_list in arp_info:
        for i in arp_list.get('arp_list'):
            ip, mac, _ = i
            arp_dict.setdefault(i[1], [])
            arp_dict[mac].append([arp_list.get('hostname'), ip])

    write2db, used_mac = [], []
    for hn in mac_info:
        for vlan in hn['mac_dict']:
            for item in hn['mac_dict'][vlan]:
                mac_addr, inftc_name = item[0], item[-1]
                used_mac.append(mac_addr)
                # TODO: add index.
                interface_desc = basic_dict.get(hn['hostname'], {}).get(inftc_name.lower(), '')
                gateway_info = arp_dict.get(mac_addr, [])

                for ip_gw in gateway_info:
                    write2db.append((ip_gw[-1], mac_addr, vlan, hn['hostname'], inftc_name, interface_desc, ip_gw[0]))
    # for those mac who was in arp_info but not in mac_info
    for gateway in arp_info:
        for item in gateway.get('arp_list'):
            ip, mac_addr, _ = item
            if mac_addr not in used_mac:
                write2db.append((ip, mac_addr, '', '', '', '', gateway.get('hostname')))

    return write2db


def insert_db(write2db):
    """
    insert data to MySQL and close the connection
    :param write2db: data in the right form
    :return: None
    """
    con = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='front')
    cur = con.cursor()
    cmd = 'INSERT INTO gw VALUES (%s,%s,%s,%s,%s,%s,%s)'
    # set these parameters if necessary.
    cur.execute('SET GLOBAL max_allowed_packet=1073741824')
    cur.execute('SET GLOBAL CONNECT_TIMEOUT = 600')
    cur.execute('SET SESSION NET_READ_TIMEOUT = 6000')

    cur.executemany(cmd, write2db)
    con.commit()
    con.close()


def write_xls(data):
    wb = Workbook()
    ws = wb.active
    ws.append(['IP', 'MAC', 'Vlan', 'hostname', 'interface', 'int_desc', 'gateway'])

    # separate large list to small list, unnecessary for this situation though.
    # for i in range(0, len(data), size):
    #     part = data[i:i + size]
    for item in data:
        ws.append(item)

    wb.save("sample.xlsx")


if __name__ == '__main__':
    parse_result = parse_arp_mac()
    # insert_db(parse_result)
    write_xls(parse_result)
