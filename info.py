# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv

import myheaders

def get_info(url):    
    account = user = date = title = read = like = article = imgs = ''
    
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
        # 内容
        article = ''
        article_list = content.find(**{'class': 'rich_media_content'}).stripped_strings
        for a in article_list:
            article += (a + '\n')
        # 图片URL
        imgs_list = content.find_all('img')
        for i in imgs_list:
            src = i.get('data-src')
            imgs += (src + '\n') if src else ''
            
        read_like = requests.get('http://mp.weixin.qq.com/mp/getcomment'+url[25:])
        # 阅读数
        read = read_like.json()['read_num']
        # 点赞数
        like = read_like.json()['like_num']
   
    results = [account,user,date,title,read,like,article,imgs]
    with open('info.csv','a', newline='',encoding='utf-8-sig') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(results)
    
    
if __name__ == '__main__':
    with open('articles.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('http://'):
                get_info(line.strip())
                
