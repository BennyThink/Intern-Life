#!/usr/bin/python
# coding:utf-8

# Intern-Life - main.py
# 2018/04/04 11:27
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


class Retrieve(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Content-Type", "application/json")
        # I'm lazy, what if I want to click the html file:-)
        # self.set_header("Access-Control-Allow-Origin", "*")
        # self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        print('setting')
        self.write(make_json())


class Index(tornado.web.RequestHandler):

    def get(self):
        self.finish(open('templates/index.html').read())


def _make_json(db_type):
    with open('config/%s/column.json' % db_type) as f:
        column = json.load(f)
    with open('config/%s/credential.json' % db_type) as f:
        credential = json.load(f)

    label = 'MySQL' if db_type == 'mysql' else 'MongoDB'

    content = {"prop": db_type, "label": label, "db_columns": column['database'], "tb_columns": column['table'],
               "databases": [i for i in credential]}

    return content


def make_json():
    return json.dumps([_make_json('mongo'), _make_json('mysql')], ensure_ascii=False).encode('utf-8')


def make_app():
    return tornado.web.Application([
        (r'/list/', Retrieve),
        (r'/', Index),
    ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
