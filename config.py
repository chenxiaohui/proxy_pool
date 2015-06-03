#!/usr/bin/python
#coding=utf-8
#Filename:config.py
import re
seg=u"\t\t"
bar_pattern = re.compile(r'width: (\d+)%')
ip_pattern = re.compile(r'IP地址: ([\d\.]*)</b>')

def clean(text):
    """"""
    return re.sub('[\t\ \n\r]','',text)


common_conf = {
    'xpath': '//table/tbody/tr',
    'filepath':'/usr/local/nginx/html/',
    'read_func':lambda proxy: {'proxy':proxy[0].strip()},
    'file_template':u"%(proxy)s\n",
}

check_conf= dict(common_conf, **{
    'consumer_size':20,
    'producer_size':1,
    'filename':'proxy-list.txt',
    'timeout':10,
    'check_url':'http://www.myip.cn/',
    'check_func':lambda html,proxy : proxy['proxy'].split(":")[0] == ip_pattern.findall(html)[0],
})

china_conf = dict(common_conf, **{
    'url' : 'http://cn-proxy.com/',
    'parse_func':lambda item : {
        'ip':item[0].text,
        'port': item[1].text,
        'location':item[2].text,
        'speed': int(bar_pattern.findall(item[3].xpath(".//strong")[0].attrib['style'])[0]),
        'last_check':item[4].text
    },
    'filename':'china-proxy-list.txt',
    'file_template':u"%(ip)s:%(port)s" + seg + u"%(location)s" + seg + u"%(speed)s" + seg + u"%(last_check)s\n",
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
    'filename':'global-proxy-list.txt',
    'file_template':u"%(ip)s:%(port)s" + seg + u"%(location)s" + seg + u"%(speed)s" + seg + u"%(last_check)s\n",
})

ipcn_conf = dict(common_conf , **{
    'url' : 'http://proxy.ipcn.org/proxylist.html',
    'xpath': '//table/tbody/tr/td/pre',
    'parse_func':lambda item : {
        'ip':item[0].text,
        'port':item[0].text,
    },
    'filename':'ipcn-proxy-list.txt'
})

#pachong_conf = dict(common_conf, **{
    #'url':'http://pachong.org/',
    #'parse_func':lambda item : {
        #'ip':item[1].text,
        #'port': item[2].text_content(),
        #'speed':item[5].text_content()
    #},
    #'filename':'pachong-proxy-list.txt',
    #'file_template':u"%(ip)s:%(port)s" + seg + u"%(speed)s\n",
#})

kuaidaili_conf = dict(common_conf, **{
    'url':'http://www.kuaidaili.com/proxylist/%d',
    'variable':range(1,11),
    'parse_func':lambda item : {
        'ip':item[0].text,
        'port': item[1].text,
        'type': item[3].text,
        'location':item[5].text,
        'speed':item[6].text
    },
    'filename':'kuaidaili-proxy-list.txt',
    'file_template':u"%(ip)s:%(port)s" + seg + u"%(type)s" + seg + u"%(location)s" + seg + u"%(speed)s\n",
})

kjson_conf = dict(common_conf, **{
    'url':'http://www.kjson.com/proxy/index/%d',
    'variable':range(1,12),
    'xpath':'//table/tr[@class="plist tc"]',
    'parse_func':lambda item : {
        'ip':item[0].text,
        'port': item[1].text,
        'type': item[2].text,
        'anonymous':item[3].text,
    },
    'filename':'kjson-proxy-list.txt',
    'file_template':u"%(ip)s:%(port)s" + seg + u"%(type)s" + seg + u"%(anonymous)s\n",
})

cz88_conf = dict(common_conf, **{
    'url':'http://www.cz88.net/proxy/',
    'xpath':'//div[@class="box694"]/ul/li[position()>1]',
    'parse_func':lambda item : {
        'ip':item[0].text,
        'port': item[1].text,
        'type': item[2].text,
        'anonymous':item[3].text,
    },
    'filename':'cz88-proxy-list.txt',
    'file_template':u"%(ip)s:%(port)s" + seg + u"%(type)s" + seg + u"%(anonymous)s\n",
})

cz88_other_conf = dict(cz88_conf, **{
    'url':'http://www.cz88.net/proxy/http_%d.shtml',
    'xpath':'//div[@class="box694"]/ul/li[position()>1]',
    'variable':range(2,11),
    'parse_func':lambda item : {
        'ip':item[0].text,
        'port': item[1].text,
        'type': item[2].text,
        'anonymous':item[3].text,
    },
    'filename':'cz88-other-proxy-list.txt',
    'file_template':u"%(ip)s:%(port)s" + seg + u"%(type)s" + seg + u"%(anonymous)s\n",
})
#if __name__ == '__main__':
    #conf = common_conf
    #html = ' <h2><b>IP地址: 123.134.186.159</b></h2>'
    #print conf['check_func'](html,{'proxy':'123.134.186.159:18'})
