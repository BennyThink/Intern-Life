#!/usr/bin/python
# coding:utf-8

import json
import re
from openpyxl import Workbook

import mysql.connector


def read_file(filename):
    with open(filename) as f:
        return json.load(f)[0].get('data')


def generate_basic_dict(basic_info):
    """
    generate a dict according to basic_info.json, provide searching for interface description
    :param basic_info: raw file
    :return: a dict like {'JD70SW24-B1-VDC2': {'ethernet4/11': 'this is description',{'12331221':3066}}
    """

    basic_dict = {}
    for hn in basic_info:
        basic_dict.setdefault(hn.get('hostname'), {})
        for index in hn.get('if_index'):
            if index in hn.get('if_desc'):
                # index in arp_info
                basic_dict[hn.get('hostname')].update(
                    {hn.get('if_index').get(index).lower(): [index, hn.get('if_desc').get(index)],
                     index: extract_vlan_num(hn.get('if_index').get(index))})

    return basic_dict


def generate_arp_dict(arp_info):
    """
    generate arp dict according to arp_info.json
    :param arp_info: raw file
    :return: dict
    """
    arp_dict = {}
    # generate arp_dict, the key is mac address, value is ['hostname1, hostname2', 'IP', 'index'].
    for arp_list in arp_info:
        for i in arp_list.get('arp_list'):
            ip, mac, index = i

            arp_dict.setdefault(i[1], [])
            # Merge gateway.
            if len(arp_dict[mac]) == 0:
                arp_dict[mac].append([arp_list.get('hostname'), ip, index])
            elif ip == arp_dict[mac][0][1] and index == arp_dict[mac][0][2]:
                arp_dict[mac][0][0] = arp_dict[mac][0][0] + ',' + arp_list.get('hostname')
            else:
                arp_dict[mac].append([arp_list.get('hostname'), ip, index])

    return arp_dict


def extract_vlan_num(vlan_str):
    """
    extract vlan numbers
    :param vlan_str: vlan string
    :return: int, vlan number
    """
    regex = re.compile(r"Vlan\s?(\d+)", re.I)
    result = regex.findall(vlan_str)
    if result:
        return result[0]
    else:
        return ''


def parse_arp_mac(arp_info, arp_dict, basic_dict, mac_info, ):
    """
    parse arp and mac in three different situation
    :param arp_info: arp_info.json
    :param arp_dict: generated arp_dict mapping
    :param basic_dict: generated basic_dict mapping
    :param mac_info: mac_info.json
    :return: result to be written to database or Excel
    """
    write2db, used_mac = [], []
    for hn in mac_info:
        for vlan in hn['mac_dict']:
            for item in hn['mac_dict'][vlan]:
                mac_address, interface_name = item[0], item[-1]
                used_mac.append(mac_address)
                # index shouldn't be interface_desc[0]
                interface_desc = basic_dict.get(hn['hostname'], {}).get(interface_name.lower(), ['', ''])
                # two forms:1. ['h1,h2','ip','index']  2. ['h1','ip','index']
                gateway_info = arp_dict.get(mac_address, [])

                if len(gateway_info) == 0:
                    write2db.append(
                        ('', mac_address, vlan, hn['hostname'], interface_name, '',
                         interface_desc[1], ''))
                # filter by the corresponding interface of vlan
                else:
                    # use comma to separate gateway and save it as one.
                    for gw_ip_index in gateway_info:
                        if ',' in gw_ip_index[0]:
                            write2db.append(
                                (gw_ip_index[1], mac_address, vlan, hn['hostname'], interface_name, gw_ip_index[-1],
                                 interface_desc[1], gw_ip_index[0]))
                        elif vlan == basic_dict[gw_ip_index[0]].get(gw_ip_index[-1]):
                            write2db.append(
                                (gw_ip_index[1], mac_address, vlan, hn['hostname'], interface_name, gw_ip_index[-1],
                                 interface_desc[1], gw_ip_index[0]))

    # for those mac who was in arp_info but not in mac_info
    for gateway in arp_info:
        for item in gateway.get('arp_list'):
            ip, mac_address, index = item
            if mac_address not in used_mac:
                write2db.append((ip, mac_address, '', '', '', index, '', gateway['hostname']))

    return write2db


def insert_db(write2db):
    """
    insert data to MySQL and close the connection
    :param write2db: data in the right form
    :return: None
    """
    con = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='front')
    cur = con.cursor()
    cmd = 'INSERT INTO new VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    # set these parameters if necessary.
    cur.execute('SET GLOBAL max_allowed_packet=1073741824')
    cur.execute('SET GLOBAL CONNECT_TIMEOUT = 600')
    cur.execute('SET SESSION NET_READ_TIMEOUT = 6000')

    cur.executemany(cmd, write2db)
    con.commit()
    con.close()


def write_xls(data):
    """
    write data to xls
    :param data: tuple inside of list
    :return: None
    """
    # set write_only for large data set.
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    ws.append(['IP', 'MAC', 'Vlan', 'hostname', 'interface', 'index', 'int_desc', 'gateway'])

    # separate large list to small list, unnecessary for this situation though.
    # for i in range(0, len(data), size):
    #     part = data[i:i + size]
    for item in data:
        ws.append(item)

    wb.save("sample.xlsx")


if __name__ == '__main__':
    # read files
    mac_raw = read_file('mac_info.json')
    arp_raw = read_file('arp_info.json')
    basic_raw = read_file('basic_info.json')

    # generate two dict maps.
    basic_map = generate_basic_dict(basic_raw)
    arp_map = generate_arp_dict(arp_raw)

    # combine arp with mac
    parse_result = parse_arp_mac(arp_raw, arp_map, basic_map, mac_raw)

    # insert into database
    # insert_db(parse_result)

    # write into Excel
    write_xls(parse_result)
