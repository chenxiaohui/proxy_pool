#!/usr/bin/python
#coding=utf-8
#Filename:parser.py
import datetime
from urllib2 import urlopen
from config import *
import lxml.html.soupparser as soupparser
from driver import to_file
from pyvirtualdisplay import Display
from selenium import webdriver
from checker import configs


def parse(urls, conf):
    """
    parse html and get proxy list
    """
    try:
        result = []
        if 'selenium' in conf.keys() and conf['selenium']:
            display = Display(visible=0, size=(1024, 768))
            display.start()
            browser = webdriver.Firefox()
            for url in urls:
                try:
                    browser.get(url)
                except Exception , e:
                    print str(e)
                html = browser.page_source
                result.extend(dom_parse(html, conf))
            browser.quit()
            display.stop()
        else:
            for url in urls:
                try:
                    html = urlopen(url)
                except Exception , e:
                    print str(e)
                result.extend(dom_parse(html, conf))
        return result

    except Exception , e:
        raise e

def dom_parse(html, conf):
    """"""
    try:
        dom = soupparser.fromstring(html)
        items = dom.xpath(conf['xpath'])
        result = []

        for item in items:
            try:
                result.append(conf['parse_func'](item.getchildren()))
            except Exception , e:
                print str(e)

        return result
    except Exception , e:
        print str(e)

def refresh(conf):
    """
    refresh and update proxy list
    """
    try:
        template = conf['url']
        if 'variable' in conf.keys():
            proxy_list = parse([template % variable for variable in conf['variable']], conf)
        else:
            proxy_list = parse([template], conf)

        to_file(proxy_list, conf)
    except Exception , e:
        raise e

if __name__ == "__main__":
    for conf in configs:
        refresh(conf)
    #refresh(pachong_conf)
    #refresh(kjson_conf)
    print "refresh succeed. time: " + str(datetime.datetime.now())
