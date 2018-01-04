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
import json

con = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='front')
cur = con.cursor()


class Retreive(tornado.web.RequestHandler):

    def get(self):
        self.write(get_data())


class Index(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


settings = {'template_path': 'templates', 'debug': 'true',
            'static_path': os.path.join(os.path.dirname(__file__), "static")}


def make_app():
    return tornado.web.Application([
        (r'/list/', Retreive),
        (r'/', Index),
    ],
        **settings)


def get_data():
    with open('test.json', 'r') as f:
        data = f.read()
    return json.loads(data)


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
