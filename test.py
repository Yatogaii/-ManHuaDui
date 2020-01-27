import requests
import re
from Main import ManHuaDui
import base64


from Crypto.Cipher import AES
domain = r'https://www.manhuadui.com'
test_url = r'https://www.manhuadui.com/manhua/jinjidejuren/183194.html'

def getImg():
    src = r''
    res = requests.get(src)
    print(1)
    print(res.status_code)
    with open(r'img.jpg','wb+') as f:
        f.write(res.content)
        f.close()

def getHtml():
    resRequest = requests.get(test_url)
    resHtml = resRequest.text
    print(resHtml)
    return resHtml

if __name__ == '__main__':
    # txt = getHtml()
    # chapterImages = re.search('chapterPath = "[^"]*"',txt).group(0)
    # print(chapterImages)
    # #提取出加密后的文件列表，aes加密
    # chapterages = chapterImages[17:-1]
    #     # print(chapterImagesIm)
    #

    #现在只能下载一话，因为web不是连续的，有空在通过爬虫过去所有的url即可
    a = ManHuaDui(test_url,1)
    a.parseHtml()
    a.download()

    #解密成功
    # chapterImages = '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'
    # # 初始化解密器
    # key = '123456781234567G'
    # iv = 'ABCDEF1G34123412'
    # cryptos = AES.new(key.encode('utf8'),AES.MODE_CBC, iv.encode('utf8'))
    # # 优先逆向解密base64成bytes
    # data = chapterImages.encode('utf8')
    # base64_decrypted = base64.decodebytes(data)
    # # 执行解密密并转码返回str
    # decrypted_text = str(cryptos.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')
    # print(decrypted_text)