#!/usr/bin/python
#coding=utf-8
#Filename:leetcode.py
import lxml.html.soupparser as soupparser
import datetime
from urllib2 import urlopen
from config import leetcode_list_conf,seg,leetcode_page_conf
from parser import parse,to_file
import io


def get_list(conf):
    """"""
    problem_list = []
    try:
        with io.open(conf['filename']) as fp:
            lines = fp.readlines()
        for line in lines:
            item = line.strip('\n').split(seg)
            problem_list.append({
                'url':item[1],
                'title':item[0],
                'acceptance': float(item[2]),
                'difficulty': item[3]
            })
    except Exception , e:
        raise e
    return problem_list

def write_file(conf, content):
    with io.open(conf['dir'] + content['title'] + ".cpp", 'w', encoding='utf-8') as fp:
        fp.write(conf['file_template'] % content)

def crawl(conf, problem_list = None):
    """
    crawl
    """
    #for proxy in proxy_list:
    try:
        if not problem_list:
            problem_list = get_list(conf)
        for problem in problem_list:
            try:
                html = urlopen(problem['url'], timeout=10)
                dom = soupparser.fromstring(html)
                item = dom.xpath(conf['xpath'])[0]
                content = conf['parse_func'](item.getchildren())
                content['title'] = problem['title']
                write_file(conf, content)
                print problem['url']
            except Exception , e:
                print "problem:" + problem['url'] + " failed. ignore it."

    except Exception , e:
        raise e

if __name__ == "__main__":
    problem_list = parse(leetcode_list_conf)
    to_file(problem_list, leetcode_list_conf)

    #problem_list = get_list(leetcode_list_conf)
    crawl(leetcode_page_conf, problem_list)
    print "get problem list succeed. time: " + str(datetime.datetime.now())
