# coding:utf-8

import threading
from Queue import Queue


def creator(data, q):
    """
    生成用于消费的数据，等待消费者完成处理
    """
    print('Creating data and putting it on the queue')
    for item in data:
        evt = threading.Event()
        q.put((item, evt))

        print('Waiting for data to be doubled')
        evt.wait()


def my_consumer(q):
    """
    消费部分数据，并做处理

    这里所做的只是将输入翻一倍

    """
    while True:
        data, evt = q.get()
        print('data found to be processed: {}'.format(data))
        processed = data * 2
        print(processed)
        evt.set()
        q.task_done()


if __name__ == '__main__':
    q = Queue()
    data = [5, 10, 13, -1]
    thread_one = threading.Thread(target=creator, args=(data, q))
    thread_two = threading.Thread(target=my_consumer, args=(q,))
    thread_one.start()
    thread_two.start()

    q.join()
