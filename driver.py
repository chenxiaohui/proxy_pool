#!/usr/bin/python
#coding=utf-8
#Filename:driver.py
#import io

def check(proxy_list, conf):
    """"""
    pass
def to_redis():
    """"""
    pass

def to_nginx(proxy_list, conf):
    """"""
    try:
        pass
        lines = [(conf['file_template']%proxy).encode('utf-8') for proxy in proxy_list]
        with open(conf['filename'], 'w') as fp:
            fp.writelines(lines)
    except Exception , e:
        raise e

