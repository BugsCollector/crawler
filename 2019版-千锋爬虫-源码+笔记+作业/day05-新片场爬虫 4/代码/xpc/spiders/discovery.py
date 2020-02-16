# -*- coding: utf-8 -*-
import re
import random
import string
import json
import scrapy
from scrapy import Request
from xpc.items import ComposerItem, PostItem, CommentItem, CopyrightItem

def strip(s):
    if s:
        return s.strip()
    return ''


def convert_int(s):
    if isinstance(s, str):
        return int(s.replace(',', ''))
    return 0


cookies = dict(
    Authorization='A37AB29030DC8844A30DC843CB30DC8B2D630DC861E78138BA33'
)


def gen_sessionid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=26))


class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['xinpianchang.com', 'openapi-vtom.vmovier.com']
    start_urls = ['http://www.xinpianchang.com/channel/index/sort-like?from=tabArticle']
    # start_urls = ['http://www.xinpianchang.com/channel/index/type-0/sort-like/duration_type-0/resolution_type-/page-21']
    page_count = 0

    # def start_requests(self):
    #     for url in self.start_urls:
    #         c = cookies.copy()
    #         c.update(PHPSESSID=gen_sessionid(),
    #                        channel_page='apU%3D')
    #         request =  Request(url, cookies=c, dont_filter=True)
    #         # request.meta['dont_merge_cookies'] = True
    #         yield request

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        self.page_count += 1
        if self.page_count >= 100:
            cookies.update(PHPSESSID=gen_sessionid())
            self.page_count = 0
        post_list = response.xpath(
            '//ul[@class="video-list"]/li')
        url = "http://www.xinpianchang.com/a%s?from=ArticleList"
        for post in post_list:
            pid = post.xpath('./@data-articleid').get()
            request = response.follow(url % pid, self.parse_post)
            request.meta['pid'] = pid
            request.meta['thumbnail'] = post.xpath('./a/img/@_src').get()
            yield request
        pages = response.xpath('//div[@class="page"]/a/@href').extract()
        for page in pages:
            yield response.follow(page, self.parse, cookies=cookies)

    def parse_post(self, response):
        pid = response.meta['pid']
        post = PostItem(pid=pid)
        post['thumbnail'] = response.meta['thumbnail']
        post['title'] = response.xpath(
            '//div[@class="title-wrap"]/h3/text()').get()
        vid, = re.findall('vid: \"(\w+)\"\,', response.text)
        video_url = 'https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource,resource_origin?'
        cates = response.xpath('//span[contains(@class, "cate")]//text()').extract()
        post['category'] = ''.join([cate.strip() for cate in cates])
        post['created_at'] = response.xpath('//span[contains(@class, "update-time")]/i/text()').get()
        post['play_counts'] = convert_int(response.xpath('//i[contains(@class, "play-counts")]/@data-curplaycounts').get())
        post['like_counts'] = convert_int(response.xpath('//span[contains(@class, "like-counts")]/@data-counts').get())
        post['description'] = strip(response.xpath('//p[contains(@class, "desc")]/text()').get())
        request = Request(video_url % vid, callback=self.parse_video)
        request.meta['post'] = post
        yield request

        comment_url = 'http://www.xinpianchang.com/article/filmplay/ts-getCommentApi?id=%s&page=1'
        request = Request(comment_url % pid, callback=self.parse_comment)
        request.meta['pid'] = pid
        yield request

        creator_list = response.xpath('//div[@class="user-team"]//ul[@class="creator-list"]/li')
        composer_url = 'http://www.xinpianchang.com/u%s?from=articleList'

        for creator in creator_list:
            cid = creator.xpath('./a/@data-userid').get()
            request = response.follow(composer_url % cid, self.parse_composer)
            request.meta['cid'] = cid
            request.meta['dont_merge_cookies'] = True
            yield request

            cr = CopyrightItem()
            cr['pcid'] = '%s_%s' % (pid, cid)
            cr['pid'] = pid
            cr['cid'] = cid
            cr['roles'] = creator.xpath('./div[@class="creator-info"]/span/text()').get()
            yield cr

    def parse_video(self, response):
        post = response.meta['post']
        result = json.loads(response.text)
        data = result['data']
        if 'resource' in data:
            post['video'] = data['resource']['default']['url']
        else:
            d = data['third']['data']
            post['video'] = d.get('iframe_url', d.get('swf', ''))
        post['preview'] = result['data']['video']['cover']
        post['duration'] = result['data']['video']['duration']
        yield post

    def parse_comment(self, response):
        result = json.loads(response.text)

        for c in result['data']['list']:
            comment = CommentItem()
            comment['uname'] = c['userInfo']['username']
            comment['avatar'] = c['userInfo']['face']
            comment['cid'] = c['userInfo']['userid']
            comment['commentid'] = c['commentid']
            comment['pid'] = c['articleid']
            comment['created_at'] = c['addtime_int']
            comment['like_counts'] = c['count_approve']
            comment['content'] = c['content']
            if c['reply']:
                comment['reply'] = c['reply']['commentid'] or 0
            yield comment

        next_page = result['data']['next_page_url']
        if next_page:
            yield response.follow(next_page, self.parse_comment)

    def parse_composer(self, response):
        banner = response.xpath('//div[@class="banner-wrap"]/@style').get()
        composer = ComposerItem()
        composer['cid'] = response.meta['cid']
        composer['banner'], = re.findall('background-image:url\((.+?)\)', banner)
        composer['avatar'] = response.xpath(
            '//span[@class="avator-wrap-s"]/img/@src').get()
        composer['name'] = response.xpath(
            '//p[contains(@class, "creator-name")]/text()').get()
        composer['intro'] = response.xpath(
            '//p[contains(@class, "creator-desc")]/text()').get()
        composer['like_counts'] = convert_int(response.xpath(
            '//span[contains(@class, "like-counts")]/text()').get())
        composer['fans_counts'] = convert_int(response.xpath('//span[contains(@class, "fans-counts")]/text()').get())
        composer['follow_counts'] = convert_int(response.xpath('//span[@class="follow-wrap"]/span[last()]/text()').get())
        composer['location'] = response.xpath(
            '//span[contains(@class,"icon-location")]/'
            'following-sibling::span[1]/text()').get() or ''
        composer['career'] = response.xpath(
            '//span[contains(@class,"icon-career")]/'
            'following-sibling::span[1]/text()').get() or ''
        yield composer