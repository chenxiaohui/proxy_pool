#!/usr/bin/python
#coding=utf-8
#Filename:config.py
import re
pattern = re.compile(r'width: (\d+)%')

common_conf = {
'xpath': '//table/tbody/tr',
'check_url':'http://www.baidu.com/',
'file_template':u"%(ip)s:%(port)s\t\t%(location)s\t\t%(speed)s\t\t%(last_check)s\n",
'reverse':False,
}

china_conf = dict(common_conf, **{
'url' : 'http://cn-proxy.com/',
    'parse_func':lambda item : {'ip':item[0].text,
                                'port': item[1].text,
                                'location':item[2].text,
                                'speed': int(pattern.findall(item[3].xpath(".//strong")[0].attrib['style'])[0]),
                                'last_check':item[4].text},
'reverse':True,
'filename':'/usr/local/nginx/html/china-proxy-list.txt'
})

global_conf = dict(common_conf , **{
'url' : 'http://cn-proxy.com/archives/218',
    'parse_func':lambda item : {'ip':item[0].text,
                                'port': item[1].text,
                                'location':item[3].text,
                                'speed': item[4].text.strip(u"毫秒"),
                                'last_check': item[5].text},
'filename':'/usr/local/nginx/html/global-proxy-list.txt'
})
