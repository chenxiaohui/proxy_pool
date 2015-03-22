#!/usr/bin/python
#coding=utf-8
#Filename:checker.py
import urllib2
import io
from config import china_conf, global_conf, seg, ip_pattern
from driver import to_file
import sys
import datetime

def read(conf):
    """
    read from file
    """
    try:
        proxy_list = []
        with io.open(conf['filename'], 'r', encoding='utf-8') as fp:
            line = fp.readline().strip("\n")
            while line:
                proxy = line.split(seg)
                proxy_list.append({'proxy':proxy[0], 'location':proxy[1],
                                   'speed':proxy[2], 'last_check':proxy[3]})
                line = fp.readline().strip("\n")
        return proxy_list
    except Exception , e:
        raise e

def check(conf):
    """
    check
    """
    #for proxy in proxy_list:
    try:
        proxy_list = read(conf)
        valid_proxy_list = []
        for proxy in proxy_list:
            #print proxy['proxy'], ' ', proxy['speed']
            try:
                proxy_handler = urllib2.ProxyHandler({"http" : 'http://' + proxy['proxy']})
                opener = urllib2.build_opener(proxy_handler).open(conf['check_url'], timeout=conf['timeout'])
                html = opener.read()
                ret_ip = ip_pattern.findall(html)[0]
                ip, port = proxy['proxy'].split(":")
                if (ret_ip == ip):
                    proxy.update({'ip':ip, 'port':port})
                    valid_proxy_list.append(proxy)
                    #print "proxy:%s  valid"%proxy['proxy']
            except Exception , e:
                #print "proxy:" + proxy['proxy'] + " failed. ignore it."
                pass

        to_file(valid_proxy_list, conf)
    except Exception , e:
        raise e


if __name__ == "__main__":
    if len(sys.argv) > 1:
        conf = china_conf if sys.argv[1] == 'china' else global_conf
        check(conf)
        print "check %s succ. time: %s" % (sys.argv[1], str(datetime.datetime.now()))
    else:
        check(china_conf)
        check(global_conf)
        print "check all succ. time: " + str(datetime.datetime.now())
