#!/usr/bin/python
# coding:utf-8

import threading
import netaddr
from measurement import exe_time
import os
from multiprocessing import Pool


def process(filename):
    csv_content = []
    with open('test_file/' + filename, 'r') as f:
        while True:
            c = f.readline()
            if c == '':
                break
            else:
                csv_content.append(netaddr.IPNetwork(c).cidr.__str__() + '\n')
                # with open('test_file_result/' + filename, 'w') as f:
                #     f.writelines(csv_content)


@exe_time
def thread_test():
    # unlimited thread
    t = None
    for i in range(len(os.listdir('test_file'))):
        t = threading.Thread(target=process, args=(os.listdir('test_file')[i],))
        t.start()
    t.join()

    # limited
    # for i in range(len(os.listdir('test_file'))):
    #     if threading.activeCount() < 4:
    #         t = threading.Thread(target=process, args=(os.listdir('test_file')[i],))
    #         t.start()


@exe_time
def normal():
    for i in range(len(os.listdir('test_file'))):
        process(os.listdir('test_file')[i])


@exe_time
def processing_test():
    pool = Pool()
    for i in range(len(os.listdir('test_file'))):
        pool.apply_async(process, args=(os.listdir('test_file')[i],))
    pool.close()
    pool.join()


if __name__ == '__main__':
    normal()
    thread_test()
    processing_test()
