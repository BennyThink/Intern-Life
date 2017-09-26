# coding:utf-8
# wrong
from multiprocessing import Pool, Manager
import netaddr


def read_csv(q):
    with open('random_ip.csv', 'r') as f:
        while True:
            c = f.readline()
            if c == '':
                break
            else:
                value = netaddr.IPNetwork(c).cidr.__str__()
                q.put(value)


def write_csv(q):
    with open('test.csv', 'w') as f:
        while True:
            f.write(q.get(True, 1) + '\n')


if __name__ == '__main__':
    q = Manager().Queue()
    pool = Pool()
    pool.apply_async(read_csv, args=(q,))
    pool.apply_async(write_csv, args=(q,))
    pool.close()
    pool.join()
