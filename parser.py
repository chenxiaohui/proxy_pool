#!/usr/bin/python
#coding=utf-8
#Filename:parser.py
import datetime
from urllib2 import urlopen
from config import china_conf, global_conf
import lxml.html.soupparser as soupparser
from driver import to_file


def parse(conf):
    """
    parse html and get proxy list
    """
    try:
        result = []
        html = urlopen(conf['url'])
        dom = soupparser.fromstring(html)
        items = dom.xpath(conf['xpath'])

        for item in items:
            result.append(conf['parse_func'](item.getchildren()))
        return result
    except Exception , e:
        raise e

def refresh(conf):
    """
    refresh and update proxy list
    """
    try:
        proxy_list = sorted(parse(conf), key=lambda item:item['speed'], reverse=conf['reverse'])
        to_file(proxy_list, conf)
    except Exception , e:
        raise e

if __name__ == "__main__":
    refresh(china_conf)
    refresh(global_conf)
    print "refresh succeed. time: " + str(datetime.datetime.now())
