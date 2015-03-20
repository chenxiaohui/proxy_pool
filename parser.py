#!/usr/bin/python
#coding=utf-8
#Filename:parser.py
import datetime
from urllib2 import urlopen
from config import china_conf, global_conf
import lxml.html.soupparser as soupparser
from driver import to_nginx

def get_url(url):
    """
    get html content from url
    """
    #check url
    try:
        data = urlopen(url)
        return data.read()
    except Exception , e:
        raise e

def parse(conf):
    """
    parse html and get proxy list
    """
    try:
        result = []
        html = get_url(conf['url'])
        dom = soupparser.fromstring(html)
        items = dom.xpath('//table/tbody/tr')

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
        to_nginx(proxy_list, conf)
    except Exception , e:
        raise e

if __name__ == "__main__":
    refresh(china_conf)
    refresh(global_conf)
    print "refresh succeed. time: " + str(datetime.datetime.now())
