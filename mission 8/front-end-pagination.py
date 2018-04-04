#!/usr/bin/python
# coding:utf-8

# Intern-Life - fast.py
# 2017/12/15 10:56
# 

__author__ = 'Benny <benny@bennythink.com>'

import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.escape import xhtml_escape as escape
import tornado.escape
import os
import mysql.connector
import json

con = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='san')
cur = con.cursor()


class Retreive(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        print 'setting'
        self.write(get_data())


class Upsert(tornado.web.RequestHandler):

    def get(self):
        self.render('show.html')

    def post(self):
        col1 = escape(self.get_argument('col1'))
        col2 = escape(self.get_argument('col2'))
        col3 = escape(self.get_argument('col3'))
        col4 = escape(self.get_argument('col4'))
        col5 = escape(self.get_argument('col5'))
        col6 = escape(self.get_argument('col6'))
        col7 = escape(self.get_argument('col7'))
        col8 = escape(self.get_argument('col8'))
        if 'create' in self.request.uri:
            cmd = "INSERT INTO gw VALUES (NULL ,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(cmd, (col2, col3, col4, col5, col6, col7, col8))
        else:
            cmd = "UPDATE gw SET ip=%s,mac=%s,vlan=%s,hostname=%s,interface=%s ,int_desc=%s ,gateway=%s WHERE id=%s"
            cur.execute(cmd, (col2, col3, col4, col5, col6, col7, col8, col1))

        con.commit()
        self.redirect('/')


class Delete(tornado.web.RequestHandler):

    def get(self):
        self.render('show.html')

    def post(self):
        cmd = "DELETE FROM gw WHERE id=%s"
        col1 = escape(self.get_argument('col1'))
        cur.execute(cmd, (col1,))
        con.commit()
        self.redirect('/')


class Index(tornado.web.RequestHandler):

    def get(self):
        self.finish(open('templates/fep.html').read())


def make_app():
    return tornado.web.Application([
        (r'/upsert/create/', Upsert),
        (r'/list/', Retreive),
        (r'/upsert/update/', Upsert),
        (r'/delete/', Delete),
        (r'/', Index),
    ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )


def get_data():
    cur.execute('SHOW COLUMNS from switch_device')
    col_data = cur.fetchall()
    col_field = [i[0] for i in col_data]

    cur.execute('SELECT * FROM switch_device')
    data = cur.fetchall()
    bulk_dic = []
    for i in range(len(data)):
        es_dic = dict(zip(col_field, data[i]))
        bulk_dic.append(es_dic)

    return json.dumps(bulk_dic)


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
