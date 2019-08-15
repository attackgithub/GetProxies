#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# 0 bug, 0 error, 0 warning

import requests

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}

def alive(url):
    proxy = {'http': url.replace('https', 'http'),
             'https': url.replace('http', 'https')
             }
    try:
        print("当前检测代理：{}".format(url))
        r = requests.get('https://www.baidu.com/',proxies=proxy,headers=headers,timeout=3)
        if r.status_code==200:
            return 200
    except:
        pass

if __name__ == '__main__':
    print(alive('http://127.0.0.1:80'))