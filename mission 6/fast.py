#!/usr/bin/python
# coding:utf-8

# Intern-Life - fast.py
# 2017/12/15 10:56
# 

__author__ = 'Benny <benny@bennythink.com>'

import tornado.ioloop
import tornado.web
import tornado.autoreload
import os
import mysql.connector

con = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='front')
cur = con.cursor()


class Create(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        col1 = self.get_argument('col1')
        col2 = self.get_argument('col2')
        col3 = self.get_argument('col3')
        col4 = self.get_argument('col4')
        col5 = self.get_argument('col5')
        col6 = self.get_argument('col6')
        col7 = self.get_argument('col7')
        # insert or update?
        sql = 'select * from test where name="%s"' % col1
        cur.execute(sql)
        data = cur.fetchall()
        if data:
            print 'update'
            sql = 'UPDATE test SET ip = "%s", vendor = "%s", platform = "%s", hardware = "%s", version = "%s", \
            lable = "%s" WHERE name = "%s"' % (col2, col3, col4, col5, col6, col7, col1)
            cur.execute(sql)
            con.commit()
        else:
            print 'insert'
            sql = 'insert into test VALUES (%s,%s,%s,%s,%s,%s,%s)'
            cur.execute(sql, (col1, col2, col3, col4, col5, col6, col7,))
            con.commit()
        self.redirect('/')


class Retreive(tornado.web.RequestHandler):

    def get(self):
        self.render('main.html', item=get_data())


class Delete(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        col1 = self.get_argument('message')
        cur.execute('delete from test WHERE name="%s"' % col1)
        con.commit()
        self.redirect('/')


settings = {'template_path': 'templates', 'debug': 'true',
            'static_path': os.path.join(os.path.dirname(__file__), "static")}


def make_app():
    return tornado.web.Application([(r'/create', Create),
                                    (r'/', Retreive),

                                    (r'/delete', Delete)],
                                   **settings)


def get_data():
    cur.execute('select * from test')
    data = cur.fetchall()
    # con.close()
    return data


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
