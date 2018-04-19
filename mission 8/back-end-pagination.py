#!/usr/bin/python
# coding:utf-8

# Intern-Life - fast.py
# 2018/04/10 11:27
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


class Retreive(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Content-Type", "application/json")
        # I'm lazy, what if I want to click the html file:-)
        # self.set_header("Access-Control-Allow-Origin", "*")
        # self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # print('setting')
        self.write(get_data())

    def post(self):
        self.set_header("Content-Type", "application/json")
        print self.request.body
        s = {"total": 873, "data": [
            {"devicename": "JD70SW32-F2-VDC3", "area": "F2", "ip": "76.97.147.108", "bootflash": "2007040",
             "hardware": "Nexus7000", "platform": "NX-OS", "version": "6.2(2a)", "location": "J6101B-J-11",
             "memory": "32745068", "slot0": "0", "id": 1, "sn": "JAF1802AHGD"},
            {"devicename": "JD70SW0A-B5-VDC2", "area": "B5", "ip": "76.97.51.2", "bootflash": "2007040",
             "hardware": "Nexus7000", "platform": "NX-OS", "version": "6.2(2a)", "location": "J6303B-K-06",
             "memory": "32745068", "slot0": "0", "id": 2, "sn": "JAF1750BPJT"},
            {"devicename": "JD70SW0A-B5-VDC3", "area": "B5", "ip": "76.97.51.3", "bootflash": "2007040",
             "hardware": "Nexus7000", "platform": "NX-OS", "version": "6.2(2a)", "location": "J6303B-K-06",
             "memory": "32745068", "slot0": "0", "id": 3, "sn": "JAF1750BPJT"},
            {"devicename": "TG30BL01-A2", "area": "A2", "ip": "10.1.72.225", "bootflash": "",
             "hardware": "WS-CBS3020-HPQ", "platform": "IOS", "version": "12.2(50)SE3", "location": "6-4E9-3",
             "memory": "131072", "slot0": "", "id": 4, "sn": "FOC1331T01F"},
            {"devicename": "NF31BL26-B3", "area": "B3", "ip": "10.250.3.28", "bootflash": "",
             "hardware": "WS-CBS3120X-S", "platform": "IOS", "version": "12.2(50)SE3", "location": "9-1A04-01",
             "memory": "262144", "slot0": "", "id": 5, "sn": "FOC1628T00B"}]}
        self.write(s)


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


def get_data():
    try:
        con.ping()
    except mysql.connector.errors.InterfaceError:
        con.reconnect()

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
