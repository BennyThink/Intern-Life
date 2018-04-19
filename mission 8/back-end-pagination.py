#!/usr/bin/python
# coding:utf-8

# Intern-Life - back-end-pagination.py.py
# 2018/04/19 11:27
# 

__author__ = 'Benny <benny@bennythink.com>'

import tornado.ioloop
import tornado.web
import tornado.autoreload
import tornado.escape
import os
import mysql.connector
import json
import config


class Retreive(tornado.web.RequestHandler):

    def post(self):
        self.set_header("Content-Type", "application/json")
        d = json.loads(self.request.body)

        index = d['data']['page']['index']
        limit = d['data']['page']['size']
        offset = (index - 1) * limit
        keyword = d['data']['search']['value']
        clause = and_or(keyword)

        if clause:
            sql = 'select * from switch_device where %s limit %s offset %s' % (clause, limit, offset)
        else:
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


def and_or(value):
    mid_values = value.split()
    columns = config.columns
    and_cond = []
    text_cond = ''
    for mid_value in mid_values:
        or_cond = []
        for col in columns:
            or_cond.append(col + ' like "%' + mid_value + '%"')
        if or_cond:
            and_cond.append(' OR '.join(or_cond))
    if and_cond:
        text_cond = '(' + ') AND ('.join(and_cond) + ')'
    return text_cond


def get_data(sql):
    con = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='san')
    cur = con.cursor()

    cur.execute('SHOW COLUMNS from switch_device')
    col_data = cur.fetchall()
    col_field = [i[0] for i in col_data]

    cur.execute(sql)
    data = cur.fetchall()
    bulk_dic = []
    for i in range(len(data)):
        es_dic = dict(zip(col_field, data[i]))
        bulk_dic.append(es_dic)

    # get count of this result
    sql = sql.replace('*', 'count(*)')
    sql = sql[:sql.index('limit')]
    cur.execute(sql)
    count = cur.fetchall()[0][0]

    con.close()
    return json.dumps(dict(total=count, data=bulk_dic))


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
