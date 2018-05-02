#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
from web3 import Web3, HTTPProvider
import arrow
from concurrent.futures import ThreadPoolExecutor


class HitDB(object):
    """撞库尝试"""
    def __init__(self, host, port):
        self.web3 = Web3(HTTPProvider("http://%s:%s" % (host, port)))
        self.string = "0123456789abcdef"

    def create(self):
        """
        创建一个随机的64位primary key
        :return:
        """
        pk = ""
        for i in range(64):
            pk += random.choice(self.string)

        return pk

    def run(self, i):
        """
        开始执行
        :return:
        """
        n = 0
        while True:
            if n % 100 == 0:
                print(i, n, arrow.now())
            pk = self.create()
            address = self.web3.personal.importRawKey(pk, "123456")
            if self.web3.eth.getBalance(address) > 0:
                print(pk, address)

            n += 1

    def pool_run(self):
        """
        通过线程池跑
        :return:
        """
        pool = ThreadPoolExecutor(max_workers=10)
        for i in range(10):
            pool.submit(self.run, i)


def main():
    hit = HitDB("192.168.7.125", 8545)
    hit.pool_run()


if __name__ == "__main__":
    main()
    