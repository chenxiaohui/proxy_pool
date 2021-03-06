#!/usr/bin/python
#coding=utf-8
#Filename:parser.py
import datetime
from urllib2 import urlopen
from config import *
import lxml.html.soupparser as soupparser
from driver import to_file
from checker import configs


def parse(url, conf):
    """
    parse html and get proxy list
    """
    try:
        result = []
        html = urlopen(url)
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
        if 'variable' in conf.keys():
            proxy_list = []
            for variable in conf['variable'] :
                proxy_list.extend(parse(conf['url'] % variable, conf))
        else:
            proxy_list = parse(conf['url'], conf)

        to_file(proxy_list, conf)
    except Exception , e:
        raise e

if __name__ == "__main__":
    for conf in configs:
        refresh(conf)
    print "refresh succeed. time: " + str(datetime.datetime.now())
