#!/usr/bin/python
#  coding:utf-8

# import data from MySQL to MongoDB,
# clear MongoDB,
# search according to IP and device name(regex)

import mysql.connector
from pymongo import MongoClient, errors
import pprint


mongo_client = MongoClient('127.0.0.1', username='root', password='***REMOVED***123',
                           authMechanism='SCRAM-SHA-1')
db = mongo_client['san']
col = db['san_device']


def read_mysql():
    # read from MySQL and  insert into MongoDB one by one
    con = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='san')

    cur = con.cursor()
    cur.execute('select * from san_device')
    data = cur.fetchall()
    mongo_dic = {}
    for i in range(len(data)):
        mongo_dic.update(id=data[i][0], devicename=data[i][1], domainid=data[i][2],
                         ip=data[i][3], cp0ip=data[i][4], cp1ip=data[i][5],
                         location=data[i][6], hasfillword=data[i][7],
                         username=data[i][8], password=data[i][9],
                         firmware=data[i][10], vfname=data[i][11], slotinfo=data[i][12],
                         switchrole=data[i][13], zoning=data[i][14], wwn=data[i][15],
                         area=data[i][16], factory=data[i][17])

        write_mongo(mongo_dic)
    con.close()
    mongo_client.close()


def write_mongo(data_dic):
    try:
        # use copy() to prevent from Duplicate Key Error
        col.insert(data_dic.copy())
    except errors.PyMongoError as e:
        print 'Operation failed...', e
    else:
        print 'Operation succeed'


def remove_all_document():
    try:
        col.remove()
    except errors.PyMongoError as e:
        print 'Operation failed...', e
    else:
        print 'Operation succeed'
    finally:
        mongo_client.close()


def ip_query(ip):
    ip_query_result = col.find_one({'ip': ip})
    if ip_query_result is None:
        print 'No such IP...'
    else:
        pprint.pprint(ip_query_result)


def dn_query(dn):
    dn_query_result = col.find({'devicename': {'$regex': dn}})
    if dn_query_result is None:
        print 'No such device...'
    else:
        for post in dn_query_result:
            pprint.pprint(post)


if __name__ == '__main__':

    print '---------------------------------------------'
    print 'select your actions ^_^'
    print '1. import data from MySQL to Mongodb'
    print '2. remove all documents in Mongodb'
    print '3. query by IP in Mongodb'
    print '4. query by device name(regex) in Mongodb'
    print '---------------------------------------------'

    choice = input('>')
    if choice == 1:
        read_mysql()
    elif choice == 2:
        remove_all_document()
    elif choice == 3:
        ip_query(raw_input('Input your IP>>'))
    elif choice == 4:
        dn_query(raw_input('Input your regex expression>>'))
    else:
        print 'Uhh...Wrong choice. Exit now.'
