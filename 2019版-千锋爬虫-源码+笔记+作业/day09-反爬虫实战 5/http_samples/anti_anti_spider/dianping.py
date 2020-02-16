import os
import re
import requests
from pprint import pprint
from urllib.request import urlretrieve
from lxml import etree
import lxml.html
import tinycss
from tinycss.token_data import ContainerToken, TokenList


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
url = 'http://www.dianping.com/shop/113942879'
r = requests.get(url, headers=headers)
index = r.text.find('flora_3659')
print(r.text[index: index+1500])

selector = etree.HTML(r.text)
plist = selector.xpath('//ul[@id="reviewlist-wrapper"]/li//p[@class="desc"]')
for p in plist:
    # 把节点对象转换成html源码
    source = lxml.html.tostring(p, encoding='unicode')
    # 去掉源码里最外面的p标签
    source = source[16:-5]
    # 替换掉内部的span标签
    text = re.sub(r'<span class=\"([a-zA-Z0-9\-]+)\"></span>', r'{{\1}}', source)
    print(text)

# 请求CSS文件
css_url = selector.xpath('//link[contains(@href, "svgtextcss")]/@href')[0]
print(css_url)
css_resp = requests.get('http:' + css_url)
# 解析CSS文件
parser = tinycss.make_parser('page3')
ss = parser.parse_stylesheet(css_resp.text)
css_dict = {}
for rule in ss.rules:
    # for selector in rule.selector:
    #     if isinstance(selector, ContainerToken):
    #         print(selector)
    #         continue
    # css_class = selector.value
    selector = rule.selector[-1]
    if isinstance(selector, ContainerToken):
        css_class = selector.content[-1].value[:-1]
    else:
        css_class = selector.value
    css_dict[css_class] = {}
    for d in rule.declarations:
        lst = []
        for v in d.value:
            if v.value == ' ':
                continue
            lst.append(v.value)
        css_dict[css_class][d.name] = lst
pprint(css_dict)


svg2char = {}

from lxml import etree
# svg_path = os.path.join('./svg/', svg_filename)
# svg_url = '//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/6874cf9fc2cc7a9182b72d3a8eaed788.svg'


def download_svg(svg_url):
    svg_filename = os.path.basename(svg_url)
    svg_path = os.path.join('./svg/', svg_filename)
    urlretrieve('http:' + svg_url, svg_path)


for k, data in css_dict.items():
    if 'background-image' in data:
        download_svg(data['background-image'][0])