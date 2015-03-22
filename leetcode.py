#!/usr/bin/python
#coding=utf-8
#Filename:leetcode.py

import urllib2
import sys
import datetime
from checker import read
import lxml.html.soupparser as soup
from config import leetcode_conf


#def crawl(conf):
    #"""
    #crawl
    #"""
    ##for proxy in proxy_list:
    #try:
        #proxy_list = read(conf)
        #for proxy in proxy_list:
            ##print proxy['proxy'], ' ', proxy['speed']
            #try:
                #proxy_handler = urllib2.ProxyHandler({"http" : 'http://' + proxy['proxy']})
                #opener = urllib2.build_opener(proxy_handler).open(conf['check_url'], timeout=conf['timeout'])
                #html = opener.read()
                #ret_ip = ip_pattern.findall(html)[0]
                #ip, port = proxy['proxy'].split(":")
                #if (ret_ip == ip):
                    #proxy.update({'ip':ip, 'port':port})
                    #valid_proxy_list.append(proxy)
                    ##print "proxy:%s  valid"%proxy['proxy']
            #except Exception , e:
                ##print "proxy:" + proxy['proxy'] + " failed. ignore it."
                #pass

    #except Exception , e:
        #raise e
def parse_proj_list(conf = leetcode_conf):
    """"""
    try:
        problem_list = []
        html = urllib2.urlopen(conf['list-url'])
        dom = soup.fromstring(html.read())
        items = dom.xpath(conf['list-xpath'])
        for item in items:
            problem_list.append(conf['list_parse_func'](item.getchildren()))
    except Exception , e:
        raise e

if __name__ == "__main__":
    #if len(sys.argv) > 1:
        #print "check %s succ. time: %s" % (sys.argv[1], str(datetime.datetime.now()))
    #else:
        #print "check all succ. time: " + str(datetime.datetime.now())

    parse_proj_list()
