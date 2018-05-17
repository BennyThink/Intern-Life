#!/usr/bin/python
# coding:utf-8

# Intern-Life - main.py
# 2018/04/04 11:27
#
from typing import Any, Union

__author__ = 'Benny <benny@bennythink.com>'

import json
import os
import re

import tornado.escape
import tornado.ioloop
import tornado.web

from mission9 import db

PATH = os.path.split(os.path.realpath(__file__))[0]
NAME = dict(mysql='MySQL', mongo='MongoDB', elasticsearch='ElasticSearch', postgresql='PostgreSQL',
            mariadb='MariaDB', mssql='MS SQL Server', cassandra='Cassandra', redis='Redis')


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


class TableAdd(tornado.web.RequestHandler):

    def post(self):
        d = json.loads(self.request.body)
        index = _add_table(d)
        self.write(json.dumps({'status': '0', 'index': index, 'message': '写入json文件成功'}))


def _add_table(data):
    i = 0
    db_folder = data['db_type']
    with open('config/%s/credential.json' % db_folder, 'r+', encoding='utf-8') as f:
        old = json.load(f)
        data.pop('db_type')

        for item in old:
            if item['database'] == data['server'][0] and item['host'] == data['server'][1] and item['port'] == \
                    data['server'][2]:
                item['tables'].append(data['tables'])
                break
            else:
                i += 1

        f.seek(0)
        f.truncate()
        f.write(json.dumps(old, ensure_ascii=False))

        return i


def _add_credential(data):
    db_folder = data['db_type']
    with open('config/%s/credential.json' % db_folder, 'r+', encoding='utf-8') as f:
        old = json.load(f)
        data.pop('db_type')
        data['tables'] = []
        data['white_list'] = []
        old.append(data)

        f.seek(0)
        f.truncate()
        f.write(json.dumps(old, ensure_ascii=False))


class Index(tornado.web.RequestHandler):

    def get(self):
        self.finish(open('templates/index.html', encoding='utf-8').read())


def _make_json(db_type):
    """

    :param db_type:
    :return: dict
    """
    with open(PATH + '/config/%s/column.json' % db_type, encoding='utf-8') as f:
        column = json.load(f)
    with open(PATH + '/config/%s/credential.json' % db_type, encoding='utf-8') as f:
        credential = json.load(f)

    content = {"prop": db_type, "label": NAME.get(db_type, db_type), "db_columns": column['database'],
               "tb_columns": column['table'],
               "databases": [i for i in credential]}

    # filter goes here, content is the data.
    return table_filter(content, True)
    # return content


def make_json(db_folder):
    """

    :param db_folder:
    :return: str
    """
    return json.dumps([_make_json(i) for i in db_folder], ensure_ascii=False)


def make_app():
    return tornado.web.Application([
        (r'/list/', Retrieve),
        (r'/', Index),
        (r'/database/add/', DbAdd),
        (r'/table/add/', TableAdd),
    ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )


def table_filter(data, enable=True):
    if not enable:
        return data

    for item in data['databases']:
        # item a whole database
        # print(item['tables'])
        new = []
        for tb in item['tables']:

            for regex in item['white_list']:
                # print(regex)
                if re.compile(regex).findall(tb['table_name']):
                    # find

                    new.append(tb)
                    item['tables'] = new
                    # item['tables'] = [tb]
                    # print(item)
    # data seems right...? only the last data. okay,right now.

    return data


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
