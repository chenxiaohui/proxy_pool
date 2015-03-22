#!/usr/bin/python
#coding=utf-8
#Filename:config.py
import re
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
