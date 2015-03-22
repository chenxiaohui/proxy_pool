#!/usr/bin/python
#coding=utf-8
#Filename:driver.py
import io

def to_redis():
    """"""
    pass

def to_file(proxy_list, conf):
    """"""
    try:
        pass
        lines = [conf['file_template']%proxy for proxy in proxy_list]
        with io.open(conf['filename'], 'w', encoding='utf-8') as fp:
            fp.writelines(lines)
    except Exception , e:
        raise e

