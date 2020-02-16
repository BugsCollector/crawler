# -*- coding: utf-8 -*-
import scrapy
from lxml import html
from qianmu_scrapy.items import UnisersityScrapyItem
import re
from bs4 import BeautifulSoup

class QianmuSpider(scrapy.Spider):
    name = 'qianmu'
    allowed_domains = ['qianmu.org']
    # start_urls = ['http://www.qianmu.org/']
    start_urls = ['http://www.qianmu.org/ranking/1528.htm']

    @classmethod
    def __remove_p(cls, lst):
        ret = []
        for l in lst:
            ret.append(l.replace('<p>', '').replace('</p>', '').strip())
        return ret

    @classmethod
    def __remove_link(cls, lst):
        ret = []
        for l in lst:
            soup = BeautifulSoup(l)
            if soup.get_text():
                ret.append(soup.get_text())
            else:
                ret.append(l)
        return ret


    def parse_university(self, response):
        response.replace(body=response.text.replace('\t', '').replace('\r\n', ''))
        item = UnisersityScrapyItem()
        data = {}
        item['name'] = response.xpath('//div[@id="wikiContent"]/h1/text()').extract_first()
        table = response.xpath('//div[@id="wikiContent"]/div[@class="infobox"]/table')
        if table:
            table = table[0]
            keys = table.xpath('.//td[1]/p').extract()
            keys = self.__remove_p(keys)
            keys = self.__remove_link(keys)
            cols = table.xpath('.//td[2]')
            values = [' '.join(col.xpath('.//p//text()').extract_first()) for col in cols]
            if len(keys) == len(values):
                data.update(zip(keys, values))
            else:
                pass
        item['rank'] = data.get('排名')
        item['country'] = data.get('国家')
        item['state'] = data.get('州省')
        item['city'] = data.get('城市')
        item['undergraduate_num'] = data.get('本科生人数')
        item['postgraduate_num'] = data.get('研究生人数')
        item['website'] = data.get('网址')
        yield item

    def parse(self, response):
        # links = response.xpath('//div[@class="rankItem"]//td[2]//a//@href').extract()
        links = response.xpath('//div[@class="rankItem"]//tr[position()>1]//td[2]//a//@href').extract()
        for link in links:
            if not link.startswith('http://www.qianmu.org'):
                link += 'http://qianmu.org/'
            yield response.follow(link, self.parse_university)
