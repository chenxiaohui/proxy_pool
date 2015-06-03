#!/usr/bin/python
#coding=utf-8
#Filename:parser.py
import datetime
from urllib2 import urlopen
from config import *
import lxml.html.soupparser as soupparser
from driver import to_file


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
            proxy_list = parse(conf)

        to_file(proxy_list, conf)
    except Exception , e:
        raise e

if __name__ == "__main__":
    #refresh(china_conf)
    #refresh(global_conf)
    #refresh(pachong_conf)
    refresh(kuaidaili_conf)
    print "refresh succeed. time: " + str(datetime.datetime.now())
    #html="<td><script>document.write((3064^hen)+37);</script>80</td>"
    #dom = soupparser.fromstring(html)
    #print dir(dom)

