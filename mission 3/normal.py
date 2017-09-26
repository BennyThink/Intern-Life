#!/usr/bin/python
# coding:utf-8

# ip and subnet practice
# normal

import netaddr
import random
from measurement import exe_time

IP_NUM = 10000


# performance: list, + or join? Inside or outside loop?
@exe_time
def generate_ip():
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
def process_ip():
    csv_content = []
    with open('random_ip.csv', 'r') as f:
        while True:
            c = f.readline()
            if c == '':
                break
            else:
                csv_content.append(netaddr.IPNetwork(c).cidr.__str__() + '\n')
    with open('random_ip_subnet.csv', 'w') as f:
        f.writelines(csv_content)


if __name__ == '__main__':
    generate_ip()
    process_ip()
