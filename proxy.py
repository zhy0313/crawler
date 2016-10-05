# -*- coding: utf-8 -*-

import requests, re
from bs4 import BeautifulSoup

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Upgrade-Insecure-Requests': '1',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'zh-CN,zh;q=0.8',
}

urls = [
    '',
    'http://www.kxdaili.com/dailiip/1/%s.html#ip',  # index=1
    'http://www.kxdaili.com/ipList/%s.html#ip',     # index=2
    'http://www.xicidaili.com/nn/%s',               # index=3
    'http://www.mimiip.com/gngao/%s',               # index=4
    'http://www.kuaidaili.com/free/inha/%s/'        # index=5
]

# 代理ip的网站序号、爬取的页数
def get_proxies(index=2, begin=1, end=11):
    ips = []
    for i in range(begin, end):
        url = urls[index] % i
        
        r = requests.get(url, headers=headers)
        
        soup = BeautifulSoup(r.text, 'html.parser')

        if index == 3:
            table = soup.find_all(id='ip_list')        
        elif index == 4:
            table = soup.find_all('table', **{'class':'list'})
        else:
            table = soup.find_all('tbody')
        
        for i in table[0].stripped_strings:
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', i):
                ips.append('http://'+i+':')
            elif re.match(r'^\d+$', i):
                ips.append(i+'\n')
                
    with open('proxies.txt', 'w', encoding='utf-8') as f:
        for i in range(0,len(ips),2):
            f.write(ips[i]+ips[i+1])

if __name__ == '__main__':
    get_proxies()
