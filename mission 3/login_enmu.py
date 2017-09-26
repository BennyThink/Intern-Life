# coding:utf-8

import threading
from multiprocessing import Pool
import time
from measurement import exe_time


def test(i):
    print '%s - log in emulation, ' % i,
    time.sleep(1)
    print '+logged in'


@exe_time
def main1():
    for i in range(5):
        test(i)


@exe_time
def main2():
    for i in range(5):
        t = threading.Thread(target=test, args=(i,))
        t.start()


@exe_time
def main3():
    p = Pool()
    for i in range(5):
        p.apply_async(test, args=(i,))
    p.close()
    p.join()


if __name__ == '__main__':
    print '---------1-----------'
    # main1()
    print '---------2-----------'
    main2()
    print '---------3-----------'
    # main3()
