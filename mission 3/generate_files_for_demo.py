#!/usr/bin/python
# coding:utf-8

# ip and subnet practice
# normal

import random
from measurement import exe_time

IP_NUM = 10000
FILE_NUM=10
csv_content = []


@exe_time
def generate_ip():
    for i in xrange(IP_NUM):
        ip_part1 = str(random.randint(0, 255))
        ip_part2 = str(random.randint(0, 255))
        ip_part3 = str(random.randint(0, 255))
        ip_part4 = str(random.randint(0, 255))
        mask = str(random.randint(0, 32))
        csv_content.append(ip_part1 + '.' + ip_part2 + '.' + ip_part3 + '.' + ip_part4 + '/' + mask + '\n')


def write(i):
    with open('test_file/random_ip_' + str(i) + '.csv', 'w') as f:
        f.writelines(csv_content)


if __name__ == '__main__':
    generate_ip()
    for i in range(FILE_NUM):
        write(i)
