## scrapy的安装

scrapy的底层依赖于lxml, twisted, openssl，涉及到系统C库，所以有可能会导致安装失败。

````
pip install scrapy
apt install python3-scrapy
````

## scrapy命令

###创建项目

```
scrapy startproject qianmu
```

###生成spider文件

注意：爬虫名字不要和项目名字重复

```bash
#scrapy genspider [爬虫名字] [目标网站域名]
scrapy genspider usnews qianmu.iguye.com
```

### 运行爬虫

```bash
# 运行名为usnewz的爬虫
scrapy crawl usnews
# 将爬到的数据导出为Json文件
scrapy crawl usnews -o usnews.json
# 导出为csv文件
scrapy crawl usnews -o usnews.csv -t csv
# 单独运行爬虫文件
scrapy runspider usnews.py
```

调试爬虫

```bash
# 进入到scrapy控制台，使用的是项目的环境
scrapy shell
# 带一个URL参数，将会自动请求这个url，并在请求成功后进入控制台
scxrapy shell http://url.com

```

进入到控制台以后，可以使用以下函数和对象

| A        | B                                                            |
| -------- | ------------------------------------------------------------ |
| fetch    | 请求url或者Requesrt对象，注意：请求成功以后会自动将当前作用域内的request和responsne对象重新赋值 |
| view     | 用浏览器打开response对象内的网页                             |
| shelp    | 打印帮助信息                                                 |
| spider   | 相应的Spider类的实例                                         |
| settings | 保存所有配置信息的Settings对象                               |
| crawler  | 当前Crawler对象                                              |
| scrapy   | scrapy模块                                                   |



```bash
# 用项目配置下载网页，然后用浏览器打开网页
scrapy view url
# 用项目配置下载网页，然后输出至控制台
scrapy fetch url
```





