#!/usr/bin/python
# coding:utf-8

# web interface using flask
# query by IP, device name, etc...

from flask import Flask, request, url_for
import my2mo_oop

app = Flask(__name__)

mongo = my2mo_oop.Mongo('127.0.0.1', 'root', 'xxx123', 'SCRAM-SHA-1')


@app.route('/san_device')
def get_query():
    # 绕了一个大圈……
    s = mongo.get_query_everything(request.url.split('?')[1])
    return str(s)


if __name__ == '__main__':
    app.run(debug=True)
