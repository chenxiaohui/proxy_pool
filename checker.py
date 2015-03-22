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
            lines = fp.readlines()

        for line in lines:
            proxy = line.strip('\n').split(seg)
            proxy_list.append({'proxy':proxy[0].strip(), 'location':proxy[1].strip(),
                               'speed':proxy[2].strip(), 'last_check':proxy[3].strip()})
            line = fp.readline().strip("\n")
        return proxy_list
    except Exception , e:
        raise e

def check(conf, verbose=False):
    """
    check
    """
    #for proxy in proxy_list:
    try:
        proxy_list = read(conf)
        valid_proxy_list = []
        for proxy in proxy_list:
            try:
                proxy_handler = urllib2.ProxyHandler({"http" : 'http://' + proxy['proxy']})
                opener = urllib2.build_opener(proxy_handler).open(conf['check_url'], timeout=conf['timeout'])
                html = opener.read()
                ret_ip = ip_pattern.findall(html)[0]
                ip, port = proxy['proxy'].split(":")
                if (ret_ip == ip):
                    proxy.update({'ip':ip, 'port':port})
                    valid_proxy_list.append(proxy)
                    if verbose:
                        print "proxy:%s  valid"%proxy['proxy']
            except Exception , e:
                #print "proxy:" + proxy['proxy'] + " failed. ignore it."
                pass

        to_file(valid_proxy_list, conf)
    except Exception , e:
        raise e


if __name__ == "__main__":
    if '-v' in  sys.argv:
        verbose = True
    else:
        verbose = False

    if 'china' in sys.argv:
        conf = china_conf
        check(conf, verbose)
        print "check china succ.",
    elif 'global' in sys.argv:
        conf = global_conf
        check(conf, verbose)
        print "check global succ.",
    else:
        check(china_conf, verbose)
        check(global_conf, verbose)
        print "check all succ.",
    print "time: " + str(datetime.datetime.now())
