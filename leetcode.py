#!/usr/bin/python
#coding=utf-8
#Filename:leetcode.py

import sys
import datetime
#from checker import read
from config import leetcode_list_conf
from parser import parse,to_file


import urllib2
import io
from config import china_conf, global_conf, seg, ip_pattern
from driver import to_file
import sys
import datetime

def get_list(conf, problem_list = None):
    """"""
    if not problem_list:
        problem_list = []
        try:
            with io.open(conf['filename']) as fp:
                lines = fp.readlines()
            for line in lines:
                item = line.strip('\n')
                problem_list.append({
                    'url':leetcode_conf['base_url'] + item[2].getchildren()[0].attrib['href'],
                    'title':item[2].getchildren()[0].text.strip(' '),
                    'acceptance': float(item[3].text.rstrip('%')),
                    'difficulty': item[4].text
                })
    except Exception , e:
        raise e
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

if __name__ == "__main__":
    #if len(sys.argv) > 1:
        #print "check %s succ. time: %s" % (sys.argv[1], str(datetime.datetime.now()))
    #else:
        #print "check all succ. time: " + str(datetime.datetime.now())

    problem_list = parse(leetcode_list_conf)
    to_file(problem_list, leetcode_list_conf)
    print "get problem list succeed. time: " + str(datetime.datetime.now())
