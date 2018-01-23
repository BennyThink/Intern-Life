#!/usr/bin/python
# coding:utf-8

import json

import mysql.connector


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
                # index: this index is wrong.
                basic_dict[hn.get('hostname')].update(
                    {hn.get('if_index').get(index).lower(): [index, hn.get('if_desc').get(index)],
                     index: extract_vlan_num(hn.get('if_index').get(index))})

    return basic_dict


def extract_vlan_num(s):
    # wrong regex
    # r = re.compile(r"[Vlan\s](\d+)", re.I)
    # result = r.findall(s)
    # if result:
    #     return result[0]
    # else:
    #     return ''

    if 'Vlan' in s:
        return s[4:]
    elif 'VLAN' in s:
        return s.split(' ')[2]
    else:
        return ''


def parse_arp_mac():
    with open('mac_info.json') as f:
        mac_info = json.load(f)[0].get('data')
    with open('arp_info.json') as f:
        arp_info = json.load(f)[0].get('data')

    basic_dict = generate_basic_dict()
    arp_dict = {}
    # generate arp_dict, the key is mac address, value is [hostname, IP].
    for arp_list in arp_info:
        for i in arp_list.get('arp_list'):
            ip, mac, index = i

            arp_dict.setdefault(i[1], [])
            arp_dict[mac].append([arp_list.get('hostname'), ip, index])

    write2db, used_mac = [], []

    for hn in mac_info:
        for vlan in hn['mac_dict']:
            for item in hn['mac_dict'][vlan]:
                mac_address, interface_name = item[0], item[-1]
                used_mac.append(mac_address)
                # index is wrong: interface_desc[0]
                interface_desc = basic_dict.get(hn['hostname'], {}).get(interface_name.lower(), ['', ''])

                gateway_info = arp_dict.get(mac_address, [])

                if len(gateway_info) == 0:

                    write2db.append(
                        ('', mac_address, vlan, hn['hostname'], interface_name, '',
                         interface_desc[1], ''))
                # filter by the corresponding interface of vlan, how?
                else:
                    for gw_ip_index in gateway_info:

                        if vlan == basic_dict[gw_ip_index[0]].get(gw_ip_index[-1]):
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


if __name__ == '__main__':
    parse_result = parse_arp_mac()
    print len(parse_result)
    insert_db(parse_result)
