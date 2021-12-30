#!/usr/bin/env python3

import base64
import requests
import sys
import os
import operator
from cls import IsValid
from cls import LocalFile
from cls import ListFile
from cls import NetFile
from cls import PingIP

# 获取传递的参数
try:
    #0表示文件名，1后面都是参数 0.py, 1, 2, 3
    url = sys.argv[1:][0]
    if(len(sys.argv[1:]) > 1):
        url = sys.argv[1:][1]
    elif(len(sys.argv[1:]) > 2):
        url = sys.argv[1:][2]
except:
    url = 'init'

confile = './clients/config.json'
url = 'https://raw.githubusercontent.com/vpei/Free-Node-Merge/main/out/node.txt'
print('url: ' + url)

# 测试单个节点
j = 'trojan://8cf83f44-79ff-4e50-be1a-585c82338912@t2.ssrsub.com:8443?sni=douyincdn.com#v2cross.com'
onenode = PingIP.node_config_json(j, confile)
kbs = PingIP.nodespeedtest()

Departs = []#待排序列表
class Department:#自定义的元素
    def __init__(self,id,name,kbs):
        self.id = id
        self.name = name
        self.kbs= kbs

localnode = LocalFile.read_LocalFile("./node.txt")
localnode = base64.b64decode(localnode).decode("utf-8", "ignore")

clashnodes = NetFile.url_to_str(url, 240, 120)
if(IsValid.isBase64(clashnodes) and clashnodes.find('\n') == -1):
    clashnodes = base64.b64decode(clashnodes).decode("utf-8")
clashnodes = localnode.strip('\n') + '\n' + clashnodes.strip('\n')
ii = 0
allnode = ''
expire = NetFile.url_to_str('https://raw.githubusercontent.com/vpei/Free-Node-Merge/main/res/expire.txt', 240, 120)
for i in clashnodes.split('\n'):
    if(allnode.find(i) == -1 and expire.find(i) == -1):
        allnode = allnode + '\n' + i
allnode = allnode.replace(' ', '').replace('\n\n', '\n').strip('\n')
i = 0
onenode = ''
for j in clashnodes.split('\n'):
    try:
        #if(j.strip(' ') != ''):
        i += 1
        #else:
        #    continue
        onenode = PingIP.node_config_json(j, confile)
        if(onenode.find('outbound') > -1):
            ###以上已生成config.json文件###
            kbs = PingIP.nodespeedtest()
            if(kbs > 0):            
                #创建元素和加入列表
                Departs.append(Department(int(kbs), j , str(kbs)))
                print('Line-200-' + str(i) + '-已添加\nonenode:' + j + '\n')
            else:
                print('Line-202-' + str(i) + '-已出错\nonenode:' + j + '\n')
        else:
            print('Line-204-' + str(i) + '-已过滤' + '\n')
    except Exception as ex:
        print('Line-213-' + str(i) + '-Exception:' + str(ex) + '\nonenode:' + onenode + '\nj:' + j + '\n')

if(os.path.exists(confile)):
    os.remove(confile)

#划重点#划重点#划重点----排序操作
cmpfun = operator.attrgetter('id','name')#参数为排序依据的属性，可以有多个，这里优先id，使用时按需求改换参数即可
Departs.sort(key = cmpfun, reverse=True)#使用时改变列表名即可
#划重点#划重点#划重点----排序操作
 
#此时Departs已经变成排好序的状态了，排序按照id优先，其次是name，遍历输出查看结果
newallnode = ''
for depart in Departs:
    newallnode = newallnode + '\n' + depart.name
    print(str(depart.id) + '-' + depart.name + '-' + depart.kbs)
# Base64加密后保存
newallnode = base64.b64encode(newallnode.strip('\n').encode("utf-8")).decode("utf-8")
# 保留处理后的结果
if(len(newallnode) > 1024):
    LocalFile.write_LocalFile('./node.txt', newallnode) 
    print('node.txt-is-ok')
else:
    print('node.txt-is-err-filesize:' + str(len(newallnode)))