#!/usr/bin/python
# coding:utf-8

# Intern-Life - fast.py
# 2017/12/15 10:56
# 

__author__ = 'Benny <benny@bennythink.com>'

import tornado.ioloop
import tornado.web
import tornado.autoreload
import tornado.escape
import os
import mysql.connector
import json

con = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='front')
cur = con.cursor()


class Create(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')

    def post(self):
        cmd = "INSERT INTO test VALUES (%s,%s,%s,%s,%s)"
        col1 = escape(self.get_argument('col1'))
        col2 = escape(self.get_argument('col2'))
        col3 = escape(self.get_argument('col3'))
        col4 = escape(self.get_argument('col4'))
        col5 = escape(self.get_argument('col5'))
        cur.execute(cmd, (col1, col2, col3, col4, col5))
        con.commit()
        self.redirect('/')


class Retreive(tornado.web.RequestHandler):

    def get(self):
        self.write(get_data())


class Update(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')

    def post(self):
        cmd = "UPDATE test SET name=%s,ip=%s,platform=%s,hardware=%s WHERE id=%s"
        col1 = escape(self.get_argument('col1'))
        col2 = escape(self.get_argument('col2'))
        col3 = escape(self.get_argument('col3'))
        col4 = escape(self.get_argument('col4'))
        col5 = escape(self.get_argument('col5'))
        cur.execute(cmd, (col2, col3, col4, col5, col1))
        con.commit()
        self.redirect('/')


class Delete(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')

    def post(self):
        cmd = "DELETE FROM test WHERE id=%s"
        col1 = escape(self.get_argument('col1'))
        cur.execute(cmd, (col1,))
        con.commit()
        self.redirect('/')


class Index(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


def make_app():
    return tornado.web.Application([
        (r'/add/', Create),
        (r'/list/', Retreive),
        (r'/update/', Update),
        (r'/delete/', Delete),
        (r'/', Index),
    ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )


def get_data():
    cur.execute('SHOW COLUMNS from test')
    col_data = cur.fetchall()
    col_field = [i[0] for i in col_data]

    cur.execute('SELECT * FROM test')
    data = cur.fetchall()
    bulk_dic = []
    for i in range(len(data)):
        es_dic = dict(zip(col_field, data[i]))
        bulk_dic.append(es_dic)

    target = {"data": bulk_dic}
    return json.dumps(target)


def escape(bad_user):
    return tornado.escape.xhtml_escape(bad_user)


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
