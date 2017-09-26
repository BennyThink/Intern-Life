#!/usr/bin/python
# coding:utf-8

# ip and netmask practice
# normal


import netaddr
import random
import time
from measurement import exe_time

IP_NUM = 100000


@exe_time
def plus_inside():
    f = open('random_ip.csv', 'w')
    for i in xrange(IP_NUM):
        ip_part1 = str(random.randint(0, 255))
        ip_part2 = str(random.randint(0, 255))
        ip_part3 = str(random.randint(0, 255))
        ip_part4 = str(random.randint(0, 255))
        mask = str(random.randint(0, 32))
        f.write(ip_part1 + '.' + ip_part2 + '.' + ip_part3 + '.' + ip_part4 + '/' + mask + '\n')
    f.close()


@exe_time
def plus_outside():
    str_content = ''
    for i in xrange(IP_NUM):
        ip_part1 = str(random.randint(0, 255))
        ip_part2 = str(random.randint(0, 255))
        ip_part3 = str(random.randint(0, 255))
        ip_part4 = str(random.randint(0, 255))
        mask = str(random.randint(0, 32))
        str_content = str_content + ip_part1 + '.' + ip_part2 + '.' + ip_part3 + '.' + ip_part4 + '/' + mask + '\n'
    with open('random_ip.csv', 'w') as f:
        f.write(str_content)


@exe_time
def join_inside():
    f = open('random_ip.csv', 'w')

    for i in xrange(IP_NUM):
        ip_part1 = str(random.randint(0, 255))
        ip_part2 = str(random.randint(0, 255))
        ip_part3 = str(random.randint(0, 255))
        ip_part4 = str(random.randint(0, 255))
        mask = str(random.randint(0, 32))
        f.write(''.join([ip_part1, '.', ip_part2, '.', ip_part3, '.', ip_part4, '/', mask, '\n']))
    f.close()


@exe_time
def list_outside():
    csv_content = []

    for i in xrange(IP_NUM):
        ip_part1 = str(random.randint(0, 255))
        ip_part2 = str(random.randint(0, 255))
        ip_part3 = str(random.randint(0, 255))
        ip_part4 = str(random.randint(0, 255))
        mask = str(random.randint(0, 32))
        csv_content.append(ip_part1 + '.' + ip_part2 + '.' + ip_part3 + '.' + ip_part4 + '/' + mask + '\n')
    with open('random_ip.csv', 'w') as f:
        f.writelines(csv_content)


@exe_time
def per_inside():
    f = open('random_ip.csv', 'w')

    for i in xrange(IP_NUM):
        ip_part1 = str(random.randint(0, 255))
        ip_part2 = str(random.randint(0, 255))
        ip_part3 = str(random.randint(0, 255))
        ip_part4 = str(random.randint(0, 255))
        mask = str(random.randint(0, 32))
        f.write('%s.%s.%s.%s/%s' % (ip_part1, ip_part2, ip_part3, ip_part4, mask))
    f.close()


@exe_time
def per_outside():
    str_content = ''
    for i in xrange(IP_NUM):
        ip_part1 = str(random.randint(0, 255))
        ip_part2 = str(random.randint(0, 255))
        ip_part3 = str(random.randint(0, 255))
        ip_part4 = str(random.randint(0, 255))
        mask = str(random.randint(0, 32))
        str_content = str_content + '%s.%s.%s.%s/%s' % (ip_part1, ip_part2, ip_part3, ip_part4, mask)
    with open('random_ip.csv', 'w') as f:
        f.write(str_content)


if __name__ == '__main__':
    plus_inside()
    plus_outside()
    per_inside()
    per_outside()
    join_inside()
    list_outside()