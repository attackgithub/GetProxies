#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

'''
 ____       _     _     _ _   __  __           _
|  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
| |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
|  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   <
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\

'''

def run():
    fr=open('proxies.txt', 'r')
    read=fr.readlines()
    fr.close()
    res=[]
    for i in read:
        r=i.replace('\n','')
        res.append(r)
    return res


if __name__ == '__main__':
    print(run())
