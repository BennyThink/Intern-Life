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

val = [('intel', 'i7', 'i72', 'i73', 'i74', 'i75', 'i76'),
       ('amd', 'athlon', 'athlon2', 'athlon3', 'athlon4', 'athlon5', 'athlon6')]


class Index(tornado.web.RequestHandler):

    def get(self):
        self.render('main.html', item=get_data())


settings = {'template_path': 'templates', 'debug': 'true',
            'static_path': os.path.join(os.path.dirname(__file__), "static")}


def make_app():
    return tornado.web.Application([(r'/', Index), ], **settings)


def get_data():
    con = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='front')
    cur = con.cursor()
    cur.execute('select * from test')
    data = cur.fetchall()
    con.close()
    return data


if __name__ == '__main__':

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
