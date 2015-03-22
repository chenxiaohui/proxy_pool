#!/usr/bin/python
#coding=utf-8
#Filename:config.py
import re

def innertext(element):
    """"""
    return ''.join([text for text in element.itertext()])
def clean(text):
    """"""
    return re.sub('[\t\ \n]','',text)

seg=u"\t\t"
bar_pattern = re.compile(r'width: (\d+)%')
ip_pattern = re.compile(r'您的IP地址: ([\d\.]*)</b>')

common_conf = {
    'xpath': '//table/tbody/tr',
    'check_url':'http://www.myip.cn/',
    'timeout':10,
    'file_template':u"%(ip)s:%(port)s" + seg + u"%(location)s" + seg + u"%(speed)s" + seg + u"%(last_check)s\n",
    'reverse':False,
}

china_conf = dict(common_conf, **{
    'url' : 'http://cn-proxy.com/',
    'parse_func':lambda item : {
        'ip':item[0].text,
        'port': item[1].text,
        'location':item[2].text,
        'speed': int(bar_pattern.findall(item[3].xpath(".//strong")[0].attrib['style'])[0]),
        'last_check':item[4].text
    },
    'reverse':True,
    'filename':'china-proxy-list.txt'
})

global_conf = dict(common_conf , **{
    'url' : 'http://cn-proxy.com/archives/218',
    'parse_func':lambda item : {
        'ip':item[0].text,
        'port': item[1].text,
        'location':item[3].text,
        'speed': int(item[4].text.strip(u"毫秒")),
        'last_check': item[5].text
    },
    'filename':'global-proxy-list.txt'
})

leetcode_conf = dict(common_conf, **{
    'base_url': 'https://leetcode.com',
    'filename':'leetcode/list.txt',
})

leetcode_page_conf = dict(leetcode_conf, **{
    'xpath':'//div[@class="question-content"]',
    'dir':'leetcode/',
    'parse_func':lambda item : {
        'subject':''.join([innertext(it) for it in item[:-2]]).replace('\r', ''),
    },
    'file_template':u'''/*
%(subject)s
*/

#include "common.h"

class Solution {
public:

};
Solution s;

TEST(%(title)s, normal) {
}
'''
})

leetcode_list_conf = dict(leetcode_conf, **{
    'url' : 'https://leetcode.com/problemset/algorithms/',
    'parse_func':lambda item : {
        #'status':item[0].getchildren()[0].attrib['class'],
        'url':leetcode_conf['base_url'] + item[2].getchildren()[0].attrib['href'],
        'title':clean(item[2].getchildren()[0].text),
        'acceptance': float(item[3].text.rstrip('%')),
        'difficulty': item[4].text
    },
    'file_template':u"%(title)s" + seg + u"%(url)s" + seg + u"%(acceptance)s" + seg + u"%(difficulty)s\n",
})

lintcode_conf = dict(common_conf, **{
    'base_url': 'http://www.lintcode.com/en',
    'filename':'lintcode/list.txt',
})

lintcode_page_conf = dict(lintcode_conf, **{
    'xpath':'//div[@id="problem-detail"]/div[3]',
    'dir':'lintcode/',
    'parse_func':lambda item : {
        'subject':''.join([innertext(it) for it in item[1:-3]]),
    },
    'file_template':u'''/*
%(subject)s
*/

#include "common.h"

class Solution {
public:

};
Solution s;

TEST(%(title)s, normal) {
}
'''
})

lintcode_list_conf = dict(lintcode_conf, **{
    'xpath':'//div[@class="list-group list"]/a',
    'url' : 'http://www.lintcode.com/en/daily/',
    'parse_func':lambda item : {
        'url':lintcode_conf['base_url'] + item[0].getparent().attrib['href'],
        'title':clean(item[3].text),
        'acceptance': clean(item[4].text).rstrip('%'),
        'difficulty': clean(item[2].text)
    },
    'file_template':u"%(title)s" + seg + u"%(url)s" + seg + u"%(acceptance)s" + seg + u"%(difficulty)s\n",
})
