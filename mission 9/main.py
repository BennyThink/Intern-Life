#!/usr/bin/python
# coding:utf-8

# Intern-Life - main.py
# 2018/04/04 11:27
# 

__author__ = 'Benny <benny@bennythink.com>'

import json
import logging
import os

import tornado.autoreload
import tornado.escape
import tornado.ioloop
import tornado.web

import db

PATH = os.path.split(os.path.realpath(__file__))[0]
NAME = dict(mysql='MySQL', mongo='MongoDB', elasticsearch='ElasticSearch', postgresql='PostgreSQL',
            mariadb='MariaDB', mssql='MS SQL Server', cassandra='Cassandra', redis='Redis')


# logging.basicConfig(level=logging.INFO)


class Retrieve(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Content-Type", "application/json")
        db_config_dir = os.listdir(PATH + '/config')
        print('Sending table data')
        self.write(make_json(db_config_dir))


class DbAdd(tornado.web.RequestHandler):

    def post(self):
        d = json.loads(self.request.body)
        if d['db_type'] == 'mongo':
            database = db.MongoAPI(d['host'], int(d['port']), d['username'], d['password'], d['database'], d['method'])
            if database.err_code == '0':
                _add_credential(d)
            self.write(json.dumps({'status': database.err_code, 'message': database.err_msg}))

        elif d['db_type'] == 'mysql':
            database = db.MySQLAPI(d['host'], int(d['port']), d['username'], d['password'], d['database'])
            if database.err_code == '0':
                _add_credential(d)
            self.write(json.dumps({'status': database.err_code, 'message': database.err_msg}))

        elif d['db_type'] == 'redis':
            database = db.MySQLAPI(d['host'], int(d['port']), d['username'], d['password'], d['database'])
            if database.err_code == '0':
                _add_credential(d)
            self.write(json.dumps({'status': database.err_code, 'message': database.err_msg}))


def _add_credential(data):
    db_folder = data['db_type']
    with open(u'config/%s/credential.json' % db_folder, 'r') as f:
        old = json.load(f)

    data.pop('db_type')
    data['tables'] = []
    data['white_list'] = []
    old.append(data)

    with open(u'config/%s/credential.json' % db_folder, 'w') as f:
        f.write(json.dumps(old, ensure_ascii=False).encode('utf-8'))


class Index(tornado.web.RequestHandler):

    def get(self):
        self.finish(open('templates/index.html').read())


def _make_json(db_type):
    with open(PATH + '/config/%s/column.json' % db_type) as f:
        column = json.load(f)
    with open(PATH + '/config/%s/credential.json' % db_type) as f:
        credential = json.load(f)

    content = {"prop": db_type, "label": NAME.get(db_type, db_type), "db_columns": column['database'],
               "tb_columns": column['table'],
               "databases": [i for i in credential]}

    return content


def make_json(db_folder):
    return json.dumps([_make_json(i) for i in db_folder], ensure_ascii=False).encode('utf-8')


def make_app():
    return tornado.web.Application([
        (r'/list/', Retrieve),
        (r'/', Index),
        (r'/database/add/', DbAdd),
    ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
