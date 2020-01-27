import requests
import time,random
import re
from getProxyList import getProxyList
from Main import ManHuaDui

# test_url = r'https://www.manhuadui.com/manhua/jinjidejuren/'                          #https://mhcdn.manhuazj.com/images/comic/205/409262/1569990375y2gqRsaGy-EoBGIZ.jpg
# test_url = 'https://www.manhuadui.com/manhua/nvpengyoujiewoyixia/'                    #https://mhcdn.manhuazj.com/ManHuaKu/n/nvpengyoujiewoyixia/1/201930416.jpg
# test_url = 'https://www.manhuadui.com/manhua/yingfengtongxueqingchuanshangyifu/' #https://mhcdn.manhuazj.com/images/comic/205/409262/1569990375y2gqRsaGy-EoBGIZ.jpg
# test_url = 'https://www.manhuadui.com/manhua/lianaijinzhideshijie/'
# test_url = {'url' : 'https://www.manhuadui.com/manhua/nizaiyueyelishanyaoguanghui/',
#             'name' : '你在月夜里闪耀光辉'}
test_url = {'url':'https://www.manhuadui.com/manhua/LASTGAME/','name':'Last Game'}
# test_url = {'url' : 'https://www.manhuadui.com/manhua/zuyishaonvxiaocunjiang/',
#             'name' : '足艺少女小村酱'}

if __name__ == '__main__':
    proxyList = getProxyList()
    try:
        response = requests.get(test_url['url'], proxies={'http': random.choice(proxyList)}, headers={'Connection': 'close'})
    except:
        response = requests.get(test_url['url'], proxies={'http': random.choice(proxyList)}, headers={'Connection': 'close'})
        while not response.status_code == 200:
            response = requests.get(test_url['url'], proxies={'http': random.choice(proxyList)},
                                    headers={'Connection': 'close'})
            time.sleep(5)
    if not response.status_code==200:
        raise Exception
    htmlTxt = response.text
    #通过这个正则表达式可以匹配到所有话的url
    resList = re.findall('(?<=<a\shref=")[^"]*(?="\stitle="[0-9]*话)',htmlTxt)
    print(len(resList))
    print(resList)
    for i in range(0,len(resList)):
        url = r'https://www.manhuadui.com'+resList[i]
        a = ManHuaDui(url,test_url['name'],i+1,proxyList)
        if not a.parseHtml() == -1: #返回-1表示这一话没有内容
            a.download()