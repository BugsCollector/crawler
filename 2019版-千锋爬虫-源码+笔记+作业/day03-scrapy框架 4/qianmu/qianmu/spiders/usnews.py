# -*- coding: utf-8 -*-
import scrapy

from qianmu.items import UniversityItem


class UsnewsSpider(scrapy.Spider):
    name = 'usnews'
    # 允许爬url的域名必须要在此字段内
    # genspider的时候可以指定
    # 比如填iguye.com，就意味着qianmu.iguye.com和www.iguye.com下面的链接都可以爬
    allowed_domains = ['qianmu.iguye.com']
    # 爬虫的入口地址，可以写多个
    start_urls = ['http://qianmu.iguye.com/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D']

    # 当框架请求start_urls内的链接成功以后，就会调用该方法
    def parse(self, response):
        # 解析链接，并提取，extract函数返回的永远是列表，即使只有一个数据
        links = response.xpath(
            '//div[@id="content"]//tr[position()>1]'
            '/td[2]/a/@href').extract()
        for link in links:
            if not link.startswith('http://qianmu.iguye.com'):
                link = 'http://qianmu.iguye.com/%s' % link

            # 让框架继续跟随这个链接，也就是说会再次发起请求
            # 请求成功以后，会调用指定的callback函数
            yield response.follow(link, self.parse_university)

    def parse_university(self, response):
        """处理大学详情页面"""
        response = response.replace(
            body=response.text.replace('\t', '').replace('\r\n', ''))
        item = UniversityItem()
        data = {}
        item['name'] = response.xpath(
            '//div[@id="wikiContent"]/h1/text()').extract_first()
        table = response.xpath(
            '//div[@id="wikiContent"]/div[@class="infobox"]/table')
        if table:
            table = table[0]
            keys = table.xpath('.//td[1]/p/text()').extract()
            cols = table.xpath('.//td[2]')
            # 当我们确定解析出来的数据只有一个时，可以使用extract_first函数
            # 直接提取列表内的内容
            values = [' '.join(col.xpath('.//text()').extract_first()) for col in cols]
            if len(keys) == len(values):
                data.update(zip(keys, values))
        # yield出去的数据，会被框架接收，进行下一步的处理，
        # 如果没有任何处理，则会打印到控制台
        item['rank'] = data.get('排名')
        item['country'] = data.get("国家")
        item['state'] = data.get('州省')
        item['city'] = data.get('城市')
        item['undergraduate_num'] = data.get('本科生人数')
        item['postgraduate_num'] = data.get('研究生人数')
        item['website'] = data.get('网址')
        yield item