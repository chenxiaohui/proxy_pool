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
        print conf['xpath']
        items = dom.xpath(conf['xpath'])
        for item in items:
            try:
                result.append(conf['parse_func'](item.getchildren()))
            except Exception , e:
                print str(e)
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

        print proxy_list
        to_file(proxy_list, conf)
    except Exception , e:
        raise e

if __name__ == "__main__":
    conf = jyhack3_conf
    refresh(conf)

    #html = urlopen('http://www.jyhack.com/article/info-152.html')
    ##html="<td><script>document.write((3064^hen)+37);</script>80</td>"
    #dom = soupparser.fromstring(html)
    #items = dom.xpath('//table/tbody/tr')

    #result = []
    #for item in items:
        #try:
            #result.append(conf['parse_func'](item.getchildren()))
        #except Exception , e:
            #print str(e)
    #print result
