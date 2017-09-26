#!/usr/bin/python
# coding:utf-8

# wrong
import threading
import netaddr
from measurement import exe_time

wr = []
csv_content = []


def process_ip():
    with open('random_ip.csv', 'r') as f:
        while True:
            c = f.readline()
            if c == '':
                break
            else:
                csv_content.append(c)
    return csv_content


def write(p_list):
    with open('random_ip_subnet_test.csv', 'w') as f:
        f.writelines(p_list)


def parser(single_ip):
    wr.append(netaddr.IPNetwork(single_ip).cidr.__str__() + '\n')


def run_thread():
    threads = []
    for i in range(len(csv_content)):
        threads.append(threading.Thread(target=parser, args=(csv_content[i],)))
    for t in threads:
        t.start()


@exe_time
def main():
    process_ip()
    run_thread()
    write(wr)


if __name__ == '__main__':
    main()
