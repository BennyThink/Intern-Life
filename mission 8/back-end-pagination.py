#!/usr/bin/python
# coding:utf-8

# Intern-Life - fast.py
# 2018/04/10 11:27
# 

__author__ = 'Benny <benny@bennythink.com>'

import tornado.ioloop
import tornado.web
import tornado.autoreload
import tornado.escape
import os
import mysql.connector
import json

con = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='san')
cur = con.cursor()


class Retreive(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Content-Type", "application/json")
        # I'm lazy, what if I want to click the html file:-)
        # self.set_header("Access-Control-Allow-Origin", "*")
        # self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # print('setting')
        self.write(get_data())

    def post(self):
        self.set_header("Content-Type", "application/json")
        d = json.loads(self.request.body)

        index = d['data']['page']['index']
        limit = d['data']['page']['size']
        offset = (index - 1) * limit
        keyword = d['data']['search']['value']

        sql = 'select * from switch_device  limit %s offset %s' % (limit, offset)
        self.write(get_data(sql))


class Index(tornado.web.RequestHandler):

    def get(self):
        self.finish(open('templates/bep.html').read())


def make_app():
    return tornado.web.Application([
        (r'/list/', Retreive),
        (r'/', Index),
    ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )


def get_data(sql):
    cur.execute('SHOW COLUMNS from switch_device')
    col_data = cur.fetchall()
    col_field = [i[0] for i in col_data]

    cur.execute(sql)
    data = cur.fetchall()
    bulk_dic = []
    for i in range(len(data)):
        es_dic = dict(zip(col_field, data[i]))
        bulk_dic.append(es_dic)

    cur.execute('select count(*) from switch_device')
    count = cur.fetchall()[0][0]

    return json.dumps(dict(total=count, data=bulk_dic))


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
