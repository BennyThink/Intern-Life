#!/usr/bin/python
# coding:utf-8
# timing decorator

import time


def exe_time(fun):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = fun(*args, **kwargs)
        print '** ', fun.__name__, ' ** | ', time.time() - t
        return res

    return wrapper
