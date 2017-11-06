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

SIZE = 1000000
TABLE_NAME = 'wordpress'
COUNT = 5
es = Elasticsearch()


@exe_time
def bulk_read_write(db, tb):
    """
    read multiple lines from MySQL and insert it into ES
    :param db: database name, which will turn into index name in ES
    :param tb: table name, determines dict.
    :return: None
    """
    con = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database=db)
    cur = con.cursor()
    # SQL Injection. but however the format %s param doesn't work. How so???
    cur.execute('SHOW  COLUMNS from %s' % tb)
    col_data = cur.fetchall()
    col_field = [j[0] for j in col_data]

    cur.execute('SELECT * FROM %s' % tb)
    while True:
        data = cur.fetchmany(SIZE)
        if data:
            bulk_dic = []
            for j in range(len(data)):
                es_dic = dict(zip(col_field, data[j]))
                es_dic.update(_index=tb, _type='hey')
                bulk_dic.append(es_dic)
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
    con = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1',
                                  database='information_schema')
    cur = con.cursor()
    cur.execute('SELECT TABLE_NAME FROM tables WHERE table_schema = %s ORDER BY DATA_LENGTH DESC LIMIT %s', (db, count))
    return cur.fetchall()


if __name__ == '__main__':
    for i in get_table(TABLE_NAME, COUNT):
        bulk_read_write(TABLE_NAME, i[0])
