#!/usr/bin/python
# coding:utf-8

# Intern-Life - fibonacci.py
# 2017/11/16 11:15
# 

__author__ = 'Benny <benny@bennythink.com>'


def fi(x):
    if x == 0:
        return 0
    elif x == 1 or x == 2:
        return 1

    else:
        return fi(x - 1) + fi(x - 2)


def test_f1():
    assert 0 == fi(0)


def test_f2():
    assert 1 == fi(1)


def test_f4():
    assert 1 == fi(2)


def test_f5():
    assert 2 == fi(3)


def test_f6():
    assert 55 == fi(10)


def test_f7():
    assert 6765 == fi(20)


if __name__ == '__main__':
    print fi(10)
