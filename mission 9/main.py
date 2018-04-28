#!/usr/bin/python
# coding:utf-8

# Intern-Life - main.py
# 2018/04/04 11:27
# 

__author__ = 'Benny <benny@bennythink.com>'

import json
import os

import tornado.autoreload
import tornado.escape
import tornado.ioloop
import tornado.web

import db

PATH = os.path.split(os.path.realpath(__file__))[0]
STANDARD = dict(mysql='MySQL', mongo='MongoDB', elasticsearch='ElasticSearch', postgresql='PostgreSQL',
                mariadb='MariaDB', mssql='MS SQL Server', cassandra='Cassandra', redis='Redis')


class Retrieve(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Content-Type", "application/json")
        db_config_dir = os.listdir(PATH + '/config')
        self.write(make_json(db_config_dir))


class dbAdd(tornado.web.RequestHandler):

    def post(self):
        d = json.loads(self.request.body)

        if d['database'] == 'mongo':
            try:
                database = db.MongoAPI(d['host'], d['port'], d['username'], d['password'], d['database'])
            except:
                self.set_status(400)

        elif d['database'] == 'mysql':
            try:
                database = db.MySQLAPI(d['host'], d['port'], d['username'], d['password'], d['database'], d['method'])
            except:
                self.set_status(400)


class Index(tornado.web.RequestHandler):

    def get(self):
        self.finish(open('templates/index.html').read())


def _make_json(db_type):
    with open(PATH + '/config/%s/column.json' % db_type) as f:
        column = json.load(f)
    with open(PATH + '/config/%s/credential.json' % db_type) as f:
        credential = json.load(f)

    content = {"prop": db_type, "label": STANDARD.get(db_type, db_type), "db_columns": column['database'],
               "tb_columns": column['table'],
               "databases": [i for i in credential]}

    return content


def make_json(db_folder):
    return json.dumps([_make_json(i) for i in db_folder], ensure_ascii=False).encode('utf-8')


def make_app():
    return tornado.web.Application([
        (r'/list/', Retrieve),
        (r'/', Index),
        (r'/database/add/', dbAdd),
    ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
