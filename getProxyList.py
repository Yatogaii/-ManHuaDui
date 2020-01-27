import requests
import re
def getProxyList():
    url = 'https://www.xicidaili.com/'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    response = requests.get(url,headers=header)
    if not response.status_code == 200:
        print('error')
        return None
    htmlText = response.text
    ipResult = re.findall('(?<=<td>)[0-9]+.[0-9]+.[0-9]+.[0-9]+(?=</td>)',htmlText)
    portResult = re.findall('(?<=<td>)[0-9]+(?=</td>)',htmlText)
    print(len(ipResult))
    print(len(portResult))
    result = [0]*100
    print(len(result))
    for i in range(0,len(ipResult)):
        result[i] = ipResult[i]+ ':{}'.format(portResult[i])
        #print(result[i])
    return result
if __name__ == '__main__':
    getProxyList()