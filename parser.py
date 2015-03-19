#!/usr/bin/python
#coding=utf-8
#Filename:parser.py
import datetime
from urllib2 import urlopen
from config import china_conf, global_conf
import lxml.html.soupparser as soupparser
from driver import to_nginx, check

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
        check(proxy_list, conf)
        to_nginx(proxy_list, conf)
    except Exception , e:
        raise e

import unittest

class TestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRegex(self):
        html = '''
        <tr>
        <td> <strong>sss</strong> 221.10.102.203</td>
        <td>843</td>
        <td>&#22235;&#24029; &#24503;&#38451;</td>
        <td>
        <div class="graph"><strong class="bar" style="width: 41%; background:#dd5500;"><span/></strong></div>
        </td>
        <td>2015-03-19 08:42:41</td>
        </tr>

                '''
        items = soupparser.fromstring(html)
        for item in items:
            print item
            td3 = item.getchildren()[3]
            print td3.xpath(".//strong")
            #print td3.getchildren()[0].getchildren()[0].attrib


if __name__ == "__main__":
    #unittest.main()
    refresh(china_conf)
    refresh(global_conf)
    print "refresh succeed. time: " + str(datetime.datetime.now())
