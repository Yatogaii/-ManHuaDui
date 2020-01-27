import base64
import os
import time
from Crypto.Cipher import AES
import requests
import re
import random

requests.adapters.DEFAULT_RETRIES = 10
class ManHuaDui:
    #第一话的网址和一共的话数
    fitstUrl = r''
    #域名
    domain = r'https://mhcdn.manhuazj.com'
    #加密后的数据
    chapterImages = ''
    #文件路径
    path = ''
    #文件名称
    name = ''
    count = 0
    #使用代理
    proxyIpList = []

    #构造函数
    def __init__(self,path,name,count,proxyList):
        self.fitstUrl = path
        self.count = count
        self.name = name
        self.proxyIpList = proxyList

    #获取Html数据
    def getHtml(self):
        try:
            response = requests.get(self.fitstUrl, proxies={'http': random.choice(self.proxyIpList)},
                                    headers={'Connection': 'close'})
        except:
            response = requests.get(self.fitstUrl, proxies={'http': random.choice(self.proxyIpList)},
                            headers={'Connection': 'close'})
            while not response.status_code == 200:
                response = requests.get(self.fitstUrl, proxies={'http': random.choice(self.proxyIpList)},
                                headers={'Connection': 'close'})
        time.sleep(5)
        if response.status_code == 200:
            return response.text

    #解析html获得密文和路径等数据
    '''
    @操作了chapterImages、Path、Name三个类变量
    '''
    def parseHtml(self):
        text = self.getHtml()
        #三个正则表达式
        reImages = 'chapterImages = "[^"]*"'
        rePath = 'chapterPath = "[^"]*"'
        reName = 'pageTitle = "[^"]*"'
        #进行匹配

        images = re.findall(reImages,text)[0]
        path = re.search(rePath,text).group(0)
        name = re.findall(reName,text)[0]
        #对匹配结果进行切片处理
        lockData = images[len('chapterImages = "'):-1]
        self.path = path[len('chapterPath = "'):-1]
        print(lockData)
        self.chapterImages = self.str2list(self.decryption(lockData))
        if len(self.chapterImages) == 1:
            return -1
    #对数据进行解密
    def decryption(self,data):
        # aes算法加密的密钥，加密模式为CBC，偏移量为Pks7
        key = '123456781234567G'
        iv = 'ABCDEF1G34123412'
        mode = AES.MODE_CBC
        #初始化解密器
        cryptos = AES.new(key.encode('utf8'), mode, iv.encode('utf8'))
        # 优先逆向解密base64成bytes
        data = data.encode('utf8')
        base64_decrypted = base64.decodebytes(data)
        # 执行解密密并转码返回str
        decrypted_text = str(cryptos.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
        print(decrypted_text)
        return decrypted_text

    def str2list(self, str) -> list:
        end = str.find(']')             # rfind('"')也可以
        res = str[1:end-1].split(',')   #因为字符串最后会有乱码，直接通过-1之类的方法不行，所以需要找到最后一个]的位置从而确定最后一个"的位置
        for i in range(0,len(res)):
            res[i] = res[i].strip('"')
        res[-1] = res[-1].strip('"')
        print(res)
        return res

    #下载图片
    def download(self):
        cnt = 1
        print('该话共有：{}'.format(len(self.chapterImages)))
        for name in self.chapterImages:
            if re.match('https?:\\\\/\\\\/',self.chapterImages[0]) != None:   #说明是另一种,直接是下载地址'https:\\/\\/mhcdn.manhuazj.com\\/ManHuaKu\\/n\\/nvpengyoujiewoyixia\\/1\\/201930416.jpg'
                path = name.replace('\\','')
            else:
                path = self.domain + '/' + self.path + name
            self.download_signle(path, cnt)
            cnt = cnt + 1
        pass

    def download_signle(self,url, cnt):
        direct = r'F:\Commic'
        localPath = direct+ '\\'+ self.name
        if not os.path.exists(localPath):
            os.makedirs(localPath)
        localPath = direct + '\\' + self.name + '\\{}'.format(self.count)
        if not os.path.exists(localPath):
            os.makedirs(localPath)
        with open(localPath+r'\{name}.jpg'.format(name=cnt), 'wb+') as f:
            print(url)
            try:
                response = requests.get(url,proxies={'http':random.choice(self.proxyIpList)},headers = { 'Connection': 'close'})
            except :
                response = requests.get(url, proxies={'http': random.choice(self.proxyIpList)},headers = { 'Connection': 'close'})
                while not response.status_code == 200:
                    response = requests.get(url,proxies={'http':random.choice(self.proxyIpList)},headers = { 'Connection': 'close'})
                    time.sleep(5)
            f.write(response.content)
            f.close()