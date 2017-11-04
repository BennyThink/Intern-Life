#!/usr/bin/python
# coding:utf-8

# mission 4 - dsl_search.py
# 2017/10/27 9:12
# https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#the-search-object

__author__ = 'Benny <benny@bennythink.com>'

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()

# method 1 chainable
s = Search(using=client, index="my-index").query("match", name='Benny')
response = s.execute()
for hit in response:
    print(hit)

# method 2 what???? why?
s = Search(using=client, index='my-index')
s.query("match", name='Benny')
response = s.execute()
for hit in response:
    print(hit)

s = Search().query("match", title="python")
response = s.delete()
