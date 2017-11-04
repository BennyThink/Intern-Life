#!/usr/bin/python
# coding:utf-8

# Intern-Life - mysql2es_demo.py
# 2017/10/27 12:35
# 

__author__ = 'Benny <benny@bennythink.com>'

import mysql.connector
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from measurement import exe_time

SIZE = 100
es = Elasticsearch()


@exe_time
def bulk_read_write(db, tb):
    """
    read multiple lines from MySQL and insert it into ES
    :param db: database name, which will turn into index name in ES
    :param tb: table name, determine dict.
    :return: None
    """
    con = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database=db)
    cur = con.cursor()
    # SQL Injection. but however the format %s param doesn't work. How so???
    cur.execute('SHOW  COLUMNS from %s' % tb)
    col_data = cur.fetchall()
    col_field = [i[0] for i in col_data]

    cur.execute('SELECT * FROM %s' % tb)
    while True:
        data = cur.fetchmany(SIZE)
        if data:
            bulk_dic = []
            for i in range(len(data)):
                es_dic = dict(zip(col_field, data[i]))
                es_dic.update(_index=tb, _type='hey')
                bulk_dic.append(es_dic)
            helpers.bulk(es, bulk_dic)
        else:
            break
    con.close()


@exe_time
def one_by_one_read_write():
    # I totally believe this method could be deprecated
    # and should be forgot forever.
    con = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='san')
    cur = con.cursor()
    cur.execute('select * from san_device')
    data = cur.fetchall()
    test = []
    for i in range(len(data)):
        es_dic = dict(id=data[i][0], devicename=data[i][1], domainid=data[i][2],
                      ip=data[i][3], cp0ip=data[i][4], cp1ip=data[i][5],
                      location=data[i][6], hasfillword=data[i][7],
                      username=data[i][8], password=data[i][9],
                      firmware=data[i][10], vfname=data[i][11], slotinfo=data[i][12],
                      switchrole=data[i][13], zoning=data[i][14], wwn=data[i][15],
                      area=data[i][16], factory=data[i][17])
        # es.create('san', 'san_device', random.random(), es_dic)

        # id (add) first came different, then they're the same in the interval of 1. Why?
        # Why interval is 2
        test.append(id(es_dic))
    print test

    con.close()


if __name__ == '__main__':
    bulk_read_write('wordpress', 'wp_comments')
    # es.indices.delete('san')
