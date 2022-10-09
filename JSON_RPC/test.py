#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Simon Liu"

import time
import threading


def get_detail_html(url):
    print("get detail html started")
    time.sleep(2)
    print("get detail html end")


def get_detail_url(url):
    print("get detail url started")
    time.sleep(4)
    print("get detail url end")


if __name__ == "__main__":    # 函数方法 arg 为函数参数
    thread1 = threading.Thread(target=get_detail_html, args=("",))
    thread2 = threading.Thread(target=get_detail_url, args=("",))

    thread1.setDaemon(True)
    # thread2.setDaemon(True)    # 将两个线程设置为守护线程，即主线程退出，这两个子线程也退出，kill

    start_time = time.time()     # 子程开始
    thread1.start()
    thread2.start()    # 当主线程退出的时候， 子线程kill掉

    # thread1.join()
    print ("last time: {}".format(time.time()-start_time))  # 输出get detail html started
