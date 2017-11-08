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
import sys
from config import SIZE, DB_NAME, COUNT, HOST, PASS

es = Elasticsearch(timeout=300, max_retries=100, retry_on_timeout=True)


@exe_time
def bulk_read_write(db, tb):
    """
    read multiple lines from MySQL and insert it into ES
    :param db: database name, which will turn into index name in ES
    :param tb: table name, determines dict.
    :return: None
    """
    con = mysql.connector.connect(user='root', password=PASS,
                                  host=HOST,
                                  database=db, connection_timeout=600)
    cur = con.cursor()
    cur.execute("SET GLOBAL max_allowed_packet=1073741824")
    cur.execute('SET GLOBAL CONNECT_TIMEOUT = 600')
    cur.execute('SET SESSION NET_READ_TIMEOUT = 6000')
    # SQL Injection. but however the format %s param doesn't work. How so???
    cur.execute('SHOW  COLUMNS from %s' % tb)
    col_data = cur.fetchall()
    col_field = [j[0] for j in col_data]

    cur.execute('SELECT * FROM %s' % tb)
    while True:
        print '%s fetching data...' % tb
        data = cur.fetchmany(SIZE)
        if data:
            bulk_dic = []
            for j in range(len(data)):
                es_dic = dict(zip(col_field, data[j]))
                es_dic.update(_index=tb.lower(), _type='hey')
                bulk_dic.append(es_dic)
            print '%s inserting data...' % tb
            helpers.bulk(es, bulk_dic)
        else:
            break
    con.close()


def get_table(db, count):
    """
    get the biggest top `count` tables in designated database
    :param db: database name
    :param count: top count
    :return:
    """
    con = mysql.connector.connect(user='root', password=PASS,
                                  host=HOST,
                                  database='information_schema')
    cur = con.cursor()
    cur.execute('SELECT TABLE_NAME FROM tables WHERE table_schema = %s ORDER BY DATA_LENGTH DESC LIMIT %s', (db, count))
    data = cur.fetchall()
    cur.close()
    con.close()
    return data


def delete():
    for i in get_table(DB_NAME, COUNT):
        es.indices.delete(i[0])


def insert():
    for i in get_table(DB_NAME, COUNT):
        print '-----%s-----' % i[0]
        bulk_read_write(DB_NAME, i[0])


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Need parameters.'
    elif sys.argv[1] == 'delete':
        delete()
    elif sys.argv[1] == 'insert':
        insert()
    else:
        print 'Wrong parameters.'
