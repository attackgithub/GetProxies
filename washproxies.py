#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

'''
 ____       _     _     _ _   __  __           _
|  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
| |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
|  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   <
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\

'''

from alive import alive
from multiprocessing import Pool, Manager
from getproxies import setinfo


def wash(i,q):
    if alive(i):
        fw = open('proxies.txt', 'a')
        fw.write(i + '\n')
        fw.close()
    q.put(i)


#进程池管理模块
def poolmana(res):
    p = Pool(10)
    q = Manager().Queue()
    print('代理池数据清洗开始......\n耗时取决于当前代理池大小......\n请耐心等待......')
    for i in res:
        i=i.replace('\n','')
        p.apply_async(wash, args=(i,q,))
    p.close()
    p.join()

def run():
    setinfo()
    fr=open('proxies.txt','r+')
    res=fr.readlines()
    fr.truncate()
    fr.close()
    fc=open('proxiesback.txt','w')
    fc.writelines(res)
    fc.close()
    poolmana(res)
    print('代理池清洗完毕......')

if __name__ == '__main__':
    run()