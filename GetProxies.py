#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

'''
 ____       _     _     _ _   __  __           _
|  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
| |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
|  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   <
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\

'''

import re
from time import sleep
import requests
from alive import alive
from multiprocessing import Pool, Manager

version = "1.0"
banner = r'''
  ____      _     ____                _           
 / ___| ___| |_  |  _ \ _ __ _____  _(_) ___  ___ 
| |  _ / _ \ __| | |_) | '__/ _ \ \/ / |/ _ \/ __|
| |_| |  __/ |_  |  __/| | | (_) >  <| |  __/\__ \
 \____|\___|\__| |_|   |_|  \___/_/\_\_|\___||___/

                        By Tide_RabbitMask | V {} 
'''.format(version)


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
url1='http://ip.jiangxianli.com/?page=1'
url2='http://ip.jiangxianli.com/?page=2'
url3='http://ip.jiangxianli.com/?page=3'

def getinfo():
    try:
        response1 = requests.get(url1, headers=headers)
        response2 = requests.get(url2, headers=headers)
        response3 = requests.get(url3, headers=headers)
        r=(response1.text+response2.text+response3.text).replace('\n','').replace('\t','').replace(' ','')
        res = re.findall('<buttonclass="btnbtn-smbtn-copy"data-url="(.*?)"', r)
        return res
    except:
        print('网络不稳定，摸鱼ing......')

def saveinfo(i,q):
    if alive(i):
        print('获得有效代理：{}'.format(i))
        fa=open('proxiestmp.txt','a')
        fa.write(i+'\n')
        fa.close()
    else:
        pass
    q.put(i)

def setinfo():
    fw=open('proxies.txt','w')
    fw.writelines(set(open('proxiestmp.txt','r').readlines()))
    fw.close()

#进程池管理模块
def poolmana(res):
    p = Pool(30)
    q = Manager().Queue()
    for i in res:
        p.apply_async(saveinfo, args=(i,q,))
    p.close()
    p.join()


def run():
    print(banner)
    num=600              #采集次数
    print("代理池拓展开始......\n预计等待时间{}分钟......\n预计采集有效去重代理数量{}-{}+......\n".format(int(num/6),num*1,num*1000))
    for i in range(num):
        print('当前第{}次采集'.format(i+1))
        res = getinfo()
        if res:
            poolmana(res)
            setinfo()
            sleep(10)
        else:
            pass
    print("代理池拓展完成......\n有效去重代理详情已保存在proxies.txt......\n代理池调用所需api为proxies.py中的run()方法......\n玩的开心~......")



if __name__ == '__main__':
    run()