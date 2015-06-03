#!/usr/bin/python
#coding=utf-8
#Filename:checker.py
from multiprocessing import Queue
import threading
import urllib2
import io
from config import *
from driver import to_file
import sys
import datetime

queue = Queue()
result = Queue()
configs=[
    china_conf,
    global_conf,
    kuaidaili_conf,
    cz88_conf,
    cz88_other_conf
]

def read(conf):
    """
    read from file
    """
    try:
        proxy_list = []
        with io.open(conf['filepath'] + conf['filename'], 'r', encoding='utf-8') as fp:
            lines = fp.readlines()

        for line in lines:
            proxy = line.strip('\n').split(seg)
            proxy_list.append(conf['read_func'](proxy))
        return proxy_list
    except Exception , e:
        raise e

class Producer(threading.Thread):
    """"""
    def __init__(self):
        super(Producer,self).__init__()

    def run(self):
        try:
            for conf in configs:
                for proxy in read(conf):
                    queue.put(proxy)
        except Exception , e:
            print str(e)

        for i in range(0, check_conf['consumer_size']):
            queue.put(".quit")

class Consumer(threading.Thread):
    """"""
    def __init__(self, verbose):
        super(Consumer,self).__init__()
        self.verbose = verbose

    def run(self):
        while True:
            task = queue.get()
            if isinstance(task, str) and task=='.quit':
                break
            if check(task, self.verbose):
                result.put(task)

def check(proxy, verbose=False):
    """
    check
    """
    #for proxy in proxy_list:
    try:
        proxy_handler = urllib2.ProxyHandler({"http" : 'http://' + proxy['proxy']})
        opener = urllib2.build_opener(proxy_handler).open(check_conf['check_url'], timeout=check_conf['timeout'])
        html = opener.read()
        if (check_conf['check_func'](html, proxy)):
            if verbose:
                print "proxy:%s  valid"%proxy['proxy']
            return True

        return False
    except Exception:
        if verbose:
            print "proxy:" + proxy['proxy'] + " failed. ignore it."
        return False



if __name__ == "__main__":
    if '-v' in  sys.argv:
        verbose = True
    else:
        verbose = False

    consumers = [Consumer(verbose) for i in xrange(0, check_conf['consumer_size'])]
    producers = [Producer() for i in xrange(0, check_conf['producer_size'])]
    [producer.start() for producer in producers]
    [consumer.start() for consumer in consumers]
    [producer.join() for producer in producers]
    [consumer.join() for consumer in consumers]

    valid_proxy_list = []
    while True:
        try:
            valid_proxy_list.append(result.get(True, timeout=1))
        except Exception:
            break

    to_file(valid_proxy_list, check_conf)
    print "check all succ. time: " + str(datetime.datetime.now())
