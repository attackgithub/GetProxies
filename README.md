# GetProxies
RabbitMask专属代理池，献给故时鱼塘。

---
### 代理存活检测模块
```
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
```
我们可以借助常见的网站去尝试代理访问来判断代理是否存活，但有些代理可以访问百度但不一定可以访问你的目标站点，所以可以根据自己的需求变更存活检测规则。
### 数据获取与处理模块
数据获取模块采用了我们刚刚推荐的站点，而且它的机制是每隔10s会刷新一边数据，棒呆！我们根据这个特性每隔十秒获取一次数据。
```
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
```
数据存储模块会对返回结果进行存活判断，然后将有用数据丢到了一个临时文件，为什么要加这一层过渡呢？当然是让它承担日志功能与去重前备份。
```
def saveinfo(i,q):
    if alive(i):
        print('获得有效代理：{}'.format(i))
        fa=open('proxiestmp.txt','a')
        fa.write(i+'\n')
        fa.close()
    else:
        pass
    q.put(i)
```
数据梳理模块我们根据刚刚的临时文件进行set处理去重。
```
def setinfo():
    fw=open('proxies.txt','w')
    fw.writelines(set(open('proxiestmp.txt','r').readlines()))
    fw.close()
```
最后当然是一个多进程并发的调度，为什么要加入多进程？不是会sleep10s等待么？我们需要考虑到一次拿到数据后存活判断的耗时，如果这10s内没有完成存活检测（因为代理的质量原因网络延时是一定存在的）就会对下次请求造成厌恶，所以我们的多进程并发就是针对的代理存活检测模块，保证每10s一个时间单位暗示定期的完成任务。
```
#进程池管理模块
def poolmana(res):
    p = Pool(30)
    q = Manager().Queue()
    for i in res:
        p.apply_async(saveinfo, args=(i,q,))
    p.close()
    p.join()
```
### 数据清洗模块
为什么要数据清理，因为一段时间不用，代理极有可能死掉了，那就重新再检测一遍存活咯。
```
def wash(i,q):
    if alive(i):
        fw = open('proxies.txt', 'a')
        fw.write(i + '\n')
        fw.close()
    q.put(i)
```
这种东西，谁愿意等呢，多进程安排~
```
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
```
考虑到某些不可描述的以为，在数据清洗前会帮你们做个备份啦，另外还会重新从临时文件去重一次，防止遗漏。
```
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
```
### API接口
哼哼，希望大家想起它的时候，明白我做的是轮子而不是平台，所以额外开发了个接口供其它平台调度，将会返回一个极高质量的代理列表。
```
def run():
    fr=open('proxies.txt', 'r')
    read=fr.readlines()
    fr.close()
    res=[]
    for i in read:
        r=i.replace('\n','')
        res.append(r)
    return res
```
### Usage
```
python GetProxies.py  #数据采集
python washproxies.py   #数据清洗
```


### 运行展示
是的，默认采集600次，大家根据自己的需求调整就是。
```
  ____      _     ____                _
 / ___| ___| |_  |  _ \ _ __ _____  _(_) ___  ___
| |  _ / _ \ __| | |_) | '__/ _ \ \/ / |/ _ \/ __|
| |_| |  __/ |_  |  __/| | | (_) >  <| |  __/\__ \
 \____|\___|\__| |_|   |_|  \___/_/\_\_|\___||___/

                        By Tide_RabbitMask | V 1.0

代理池拓展开始......
预计等待时间100分钟......
预计采集有效去重代理数量600-600000+......

当前第1次采集
当前检测代理：http://127.0.0.1:80
```
跑出的结果以日志形式存放在tmp文件，然后去重后存入proxies.txt。

![](https://upload-images.jianshu.io/upload_images/11466123-91652eb960ec14b5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后，使用刚刚的api模块调用即可，这毕竟是个轮子，如果你想的话，花五分钟丢flask做个http接口亦可，而我这里是用来给爬虫平台做调度的,链接奉上。
>https://github.com/rabbitmask/GetProxies

那么，玩的开心。
