# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import re
import random
import time

import proxy
import myheaders
import info

import logging
logging.basicConfig(level=logging.INFO)

def get_proxy_generator(filename):
    if not filename:
        # 从网站爬取新的ip保存起来
        proxy.get_proxies()
        # 读取结果并将结果以生成器返回
        with open('proxies.txt', 'r', encoding='utf-8') as f:
            for line in f:
                yield line.strip()
    else:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                yield line.strip()

# 将搜索关键词转为可插入URL的query字段
def get_query_string(oa):
    def encode2query(match):
        return str(match.group().encode('utf-8'))[2:-1].replace(r'\x', '%').upper()
    return re.sub('[\u4e00-\u9fff]+', encode2query, oa)

url = 'http://weixin.sogou.com/weixin?type=2&query={}&ie=utf8&_sug_=n&_sug_type_=1&w=01015002&oq=&ri=16&sourceid=sugg&sut=0&sst0=1475248469610&lkt=0%2C0%2C0&p=40040108'
    
def run(oa, begin, end, using_proxies, wait_time):
    search_url = url.format(get_query_string(oa)) + '&page=' + str(begin)
    headers = myheaders.random_headers()
    
    if using_proxies:
        ip = next(proxies)
    else:
        stop = False # 用于决定对当前公众号的搜索是否停止
        
    logging.info('%s 将从第%s页到第%s页：' % (oa, begin, end-1))
    for i in range(begin, end):
        logging.info('%s 第%s页 开始' % (oa, i))
        
        page_finish = False # 用于标识当前目标页是否完成检测
        while not page_finish:
            try:
                r = requests.get(
                    search_url,
                    headers = headers,
                    proxies = {'http': ip},
                    timeout = wait_time
                ) if using_proxies else requests.get(
                    search_url,
                    headers = headers,
                    timeout = wait_time
                )

                # 解析html，获得查询结果
                soup = BeautifulSoup(r.text, 'html.parser')
                results_list = soup.find_all(**{'class': 'wx-rb wx-rb3'})
                
                # 如果查询结果为0，则提示错误信息并raise错误
                if len(results_list) == 0:
                    logging.info('%s-%s 查询异常：0结果！需要切换ip' % (oa, i))
                    raise Exception
                # 如果结果不为0
                else:
                    # 在所有搜索结果中找到正确的搜索结果，解析文章链接并将解析结果存入info.csv，同时存储文章链接作为备份
                    with open('articles_urls.txt', 'a', encoding='utf-8') as f:
                        f.write('%s - %s：\n' % (oa, i))
                        for result in results_list:
                            if result.find_all(title=oa):
                                article_url = result.h4.a['href']
                                
                                logging.info('%s-%s 正在解析文章内容，并将结果写入info.csv...' % (oa, i))
                                info.get_info(article_url)
                                
                                logging.info('%s-%s 正在备份URL...' % (oa, i))
                                f.write(article_url + '\n')
                                
                    # 完成当前页后，将当前页URL作为Referer，并找到“下一页”的URL作为下次的搜索URL。
                    headers['Referer'] = search_url
                    next_page = soup.find_all(id='sogou_next')
                    if next_page:
                        search_url = 'http://weixin.sogou.com/weixin?' + next_page[0]['href']
                    # 如果找不到“下一页”，则当前页应该为最后一页
                    else:
                        if i != end-1:
                            logging.info('%s-%s 警告：已经没有下一页了！' % (oa, i))
                            stop = True
                            
                    page_finish = True
                    logging.info('%s 第%s页 结束' % (oa, i))
                    
                    second = random.choice([2,3,4,5])
                    logging.info('%s-%s 策略性暂停%s秒' % (oa, i, second))
                    time.sleep(second)
                    
            # 连接超时或者无法获得搜索结果
            except:
                # 有使用代理ip的情况下，尝试更换存档中下一个ip。如果存档无更多ip，则自动获取更多存档。
                if using_proxies:
                    try:
                        logging.info('%s-%s 尝试获取下一个ip...' % (oa, i))
                        ip = next(proxies)
                    except StopIteration:
                        logging.info('%s-%s 已经无更多ip，正在自动爬取更多代理ip......' % (oa, i))
                        global proxies
                        proxies = get_proxy_generator(None)
                        ip = next(proxies)

                # 无使用代理ip情况下，重连或者停止
                else:
                    # 不断自动重新连接：
                    logging.info('%s-%s 当前未使用代理ip，5秒将重新尝试连接，请到网页输入验证码...' % (oa, i))
                    time.sleep(5)
                    # 不重连，而是直接停止
                    #stop = True
                    #break
        if not using_proxies and stop:
            logging.info('%s 自动停止！' % oa)
            break
            
        
# 输入公众名字列表，设定是否使用代理，可使用自己已有的代理存档，设定每个连接等待时间
def main(official_accounts, using_proxies = True, filename=None, wait_time=5):
    if using_proxies:
        global proxies
        proxies = get_proxy_generator(filename)

    for oa in official_accounts:
        # 可单独设定每个目标的起止页，使用了登录cookie则end最大101，没登录end最大为11。
        run(oa, using_proxies = using_proxies, begin=1, end=11, wait_time=wait_time)


if __name__ == '__main__':
    # 目标公众号
    official_accounts = []
    
    # 使用代理ip
    main(official_accounts)
    
    # 不使用代理ip
    #main(official_accounts, using_proxies = False)
    
