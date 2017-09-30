# coding:utf-8

import threading
from multiprocessing import Pool
import time
from measurement import exe_time


def test(i):
    # print '%s - log in emulation, ' % i,
    time.sleep(1)
    # print '+logged in'


@exe_time
def normal():
    for i in range(5):
        test(i)


@exe_time
def th():
    for i in range(5):
        global t
        t = threading.Thread(target=test, args=(i,))
        t.start()
    t.join()


@exe_time
def pro():
    p = Pool()
    for i in range(5):
        p.apply_async(test, args=(i,))
    p.close()
    p.join()


if __name__ == '__main__':
    print '---------1-----------'
    normal()
    print '---------2-----------'
    th()
    # print '---------3-----------'
    # pro()
