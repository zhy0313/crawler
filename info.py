# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv

import myheaders

def get_info(url):
    #headers = myheaders.random_headers()
    
    account = user = date = title = read = like = article = ''
    imgs = []
    
    r = requests.get(url)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    content = soup.find_all(id='img-content')
    if content:
        content = content[0]
        # 文章标题
        title = content.h2.string.strip()
        # 发布时间
        date = content.find(id='post-date').string
        # 公众号名
        user = content.find(id='post-user').string
        # 微信号
        account = content.find(**{'class': 'profile_inner'}).p.span.string
        # 消息内容
        article_list = content.find(**{'class': 'rich_media_content'}).stripped_strings
        for a in article_list:
            article += (a + '\n')
            
        # 图片URL，一个单元格存十个
        img_tags = content.find_all('img')
        l = len(img_tags)
        temp = ''
        for i in range(l):
            src = img_tags[i].get('data-src')
            temp += (src + '\n') if src else ''
            if (i % 10 == 0 and i > 0) or i == l-1:
                imgs.append(temp)
                temp = ''
            
        read_like = requests.get('http://mp.weixin.qq.com/mp/getcomment'+url[25:])
        # 阅读数
        read = read_like.json()['read_num']
        # 点赞数
        like = read_like.json()['like_num']

    results = [account,user,date,title,read,like,article]
    for i in imgs:
        results.append(i)
    with open('info.csv','a', newline='',encoding='utf-8-sig') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(results)
    
    
if __name__ == '__main__':
    with open('articles_urls.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('http://'):
                get_info(line.strip())

