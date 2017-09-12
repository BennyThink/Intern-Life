#!/usr/bin/python
# coding:utf-8

# OOP version, this code has some bad taste.
# import data from MySQL to MongoDB,
# clear MongoDB,
# search according to IP and device name(regex)

import mysql.connector
from pymongo import MongoClient, errors
import pprint


class MySQL(object):
    con = None
    cur = None

    def __init__(self, host, user, password, db):
        self.con = mysql.connector.connect(host=host, user=user, password=password, database=db)

    def read_mysql(self, mongo_instance):
        cur = self.con.cursor()
        cur.execute('select * from san_device')
        data = cur.fetchall()

        for i in range(len(data)):
            # fix solution 1: move the dic inside in order to make a new dic during each loop
            mongo_dic = {}
            mongo_dic.update(id=data[i][0], devicename=data[i][1], domainid=data[i][2],
                             ip=data[i][3], cp0ip=data[i][4], cp1ip=data[i][5],
                             location=data[i][6], hasfillword=data[i][7],
                             username=data[i][8], password=data[i][9],
                             firmware=data[i][10], vfname=data[i][11], slotinfo=data[i][12],
                             switchrole=data[i][13], zoning=data[i][14], wwn=data[i][15],
                             area=data[i][16], factory=data[i][17])
            mongo.mongo_write(mongo_dic)

    def db_close(self):
        self.con.close()


class Mongo(object):
    mongo_client = None
    col = None

    def __init__(self, host, username, password, auth):
        self.mongo_client = MongoClient(host=host, username=username, password=password,
                                        authMechanism=auth)
        self.col = self.mongo_client['san']['san_device']

    def mongo_write(self, data_dic):
        try:
            self.col.insert(data_dic)
        except errors.PyMongoError as e:
            print 'Operation failed...', e
        else:
            print 'Operation succeed'
        finally:
            del data_dic

    def remove_all_document(self):
        try:
            self.col.remove()
        except errors.PyMongoError as e:
            print 'Operation failed...', e
        else:
            print 'Operation succeed'
        finally:
            self.mongo_client.close()

    def ip_query(self, ip):
        ip_query_result = self.col.find_one({'ip': ip})
        if ip_query_result is None:
            print 'No such IP...'
        else:
            pprint.pprint(ip_query_result)

    def dn_query(self, dn):
        dn_query_result = self.col.find({'devicename': {'$regex': dn}})
        if dn_query_result is None:
            print 'No such device...'
        else:
            for post in dn_query_result:
                pprint.pprint(post)

    def db_close(self):
        self.mongo_client.close()


if __name__ == '__main__':

    print '-----OOP Version of MySQL To MongoDB---------'
    print 'select your actions ^_^'
    print '1. import data from MySQL to Mongodb'
    print '2. remove all documents in Mongodb'
    print '3. query by IP in Mongodb'
    print '4. query by device name(regex) in Mongodb'
    print '---------------------------------------------'

    sql = MySQL('127.0.0.1', 'root', 'root', 'san')
    mongo = Mongo('127.0.0.1', 'root', '***REMOVED***123', 'SCRAM-SHA-1')

    choice = input('>')
    if choice == 1:
        sql.read_mysql(mongo)
    elif choice == 2:
        mongo.remove_all_document()
    elif choice == 3:
        mongo.ip_query(raw_input('Input your IP>>'))
    elif choice == 4:
        mongo.dn_query(raw_input('Input your regex expression>>'))
    else:
        print 'Uhh...Wrong choice. Exit now.'

    sql.db_close()
    mongo.db_close()
