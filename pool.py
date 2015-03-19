#!/usr/bin/python
#coding=utf-8
#Filename:pool.py
#[
# {'ip':'', 'port':'', 'location':'', 'speed':'', 'last_check':''},
#]
global_proxy_pool = []
china_proxy_pool =  []
def get_proxy(type="global"):
    """
    select a proxy from global_proxy_pool using some strategy
    """
    pass
