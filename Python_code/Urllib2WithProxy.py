# coding=utf8
import urllib.parse
import urllib.request
import sys
import re
from test.test_mailbox import TestProxyFile
from enum import Flag
from _multiprocessing import flags
from asyncio.protocols import Protocol
from idlelib.rpc import response_queue
from pip._vendor.msgpack.fallback import xrange

def testArgument():
    #测试输入参数，只需一个参数
    if len(sys.argv) != 2:
        print(u'只需要一个参数就够了')
        tipUse()
        exit()
    else:
        print(sys.argv[1])
        TP = TestProxy(sys.argv[1])

def tipUse():
    #显示提示信息
    print(u'该程序只能输入一个参数，这参数必须是一个可用的proxy')
    print(u'usage:python testUrllib2WithProxy.py http://1.2.3.4:5')

class TestProxy(object):
    #这个类的作用是测试proxy是否有效
    def __init__(self,proxy):
        self.proxy = proxy
        self.checkProxyFormat(self.proxy)
        self.url = 'http://www.baidu.com'
        self.timeout = 5
        self.flagWorld = '百度' #在网页返回的数据中查找这个关键词
        self.useProxy(self.proxy)
    def checkProxyFormat(self,proxy):
        try:
            proxyMatch = re.compile('http[s]?://[\d]{1,3}\.[\d]{1,3]\.[\d]{1,3]}\.[\d]{1,3}:[\d]{1,5}$')
            re.search(proxyMatch,proxy).group()
        except AttributeError:
            tipUse()
            exit()
        flag = 1
        proxy = proxy.replace('//','')
        try:
            protocol=proxy.split(':')[0]
            ip = proxy.split(':')[1]
            port = proxy.split(':')[2]
        except IndexError:
            print(u'下标出界')
            tipUse()
            exit()
        flag = flag and len(proxy.split(':'))==3 and len(ip.split('.'))==4
        
        flag = ip.split('.')[0] in map(str,xrange(1,256)) and flag
        flag = ip.split('.')[1] in map(str,xrange(256)) and flag
        flag = ip.split('.')[2] in map(str,xrange(256)) and flag
        flag = ip.split('.')[3] in map(str,xrange(1,255)) and flag
        flag = Protocol in [u'http',u'https'] and flag
        flag = port in map(str,range(1,65535)) and flag
        #这里检查proxy的格式
        if flag:
            print(u'输入的http代理服务器符合标准')
        else:
            tipUse()
            exit()
    def useProxy(self,proxy):
        #利用代理访问百度，并查找关键词
        protocol = proxy.split('//')[0].replace(':','')
        ip = proxy.split('//')[1]
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({protocol:ip}))
        urllib.request.install_opener(opener)
        try:
            response=urllib.request.urlopen(self.url, timeout=self.timeout)
        except:
            print('连接错误，退出程序')
            exit()
        str = response.read()
        if re.search(self.flagWord,str):
            print(u"已取得特征词，代理可用")
        else:
            print(u'代理不可用')
if __name__ == '__main__':
    testArgument()
        