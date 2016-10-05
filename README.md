# **crawler**

微信公众号文章爬虫



通过对目标公众号进行搜索爬取，解析文章内容，摘录信息存放在文件 info.csv 中。



## 用法

### 必选项

1. 在 `myheaders.py` 的 `cookies` 中加入从自己浏览器中获取的 cookies。


2. 在主文件 `spider.py` 的最下面中加入目标公众号列表，如 `['xxxx', 'xxx']` 。



### 可选项

1. **代理ip选择**

   程序本身会自动获取代理ip，并存放在 `proxies.txt` 中；但从效率上考虑，用户也可以使用自己持有的代理ip，写在一个文本文件中，如 `example.txt` ：

   ```
   http://1.2.3.4:5555
   http://6.7.8.9:1010
   ```

   然后在 `spider.py` 最下面：

   ```python
   if __name__ == '__main__':
       # 目标公众号
       official_accounts = ['xxx']
       
       # 使用代理ip
       main(official_accounts, filename='example.txt')
   ```

   ​

2. **不使用代理**

   如果目标数很小，也可以不使用代理ip：

   ```python
   if __name__ == '__main__':
       # 目标公众号
       official_accounts = ['xxx']
       
       # 不使用代理ip
       main(official_accounts, using_proxies = False)
   ```



3. **超时设置**

   可以设定每此连接服务器的等待时间（默认5秒），超时则使用下一个代理ip或者（没代理时）自动重新连接。

   ```python
   # 等待时间：3秒
   main(official_accounts, wait_time=3)
   ```



4. **爬取的页码**

   在 `spider.py` 的 `main` 中可以单独设定目标号的查询起始页，范围是 [beging, end)。

   ```python
   for oa in official_accounts:
       # 以下表示目标xxx，从第11页到第14页；其它都从1到10。
       if oa == 'xxx':
   		run(oa, using_proxies = using_proxies, begin=11, end=15, wait_time=wait_time)
       else：
       	run(oa, using_proxies = using_proxies, begin=1, end=11, wait_time=wait_time)
   ```

   *ps. 页面最小是1，最大取决于cookies：如果使用了登录cookies，最大为101，即共有100页；如果是没登录的cookies，最大为11，即共有10页。*




## 依赖包

* requests
* BeautifulSoup



## 其它

1. 目前最大问题是代理ip的获取，自动获取的不稳定，大大影响效率，建议使用自己的代理ip。
2. 这是一个对爬虫的初学习成果，还有很多不好的地方，在以后会继续改进。