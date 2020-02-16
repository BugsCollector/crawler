import os
import urllib.request
import requests
from pprint import pprint
import parsel
from fontTools.ttLib import TTFont


BASE_FONT_PATH = './base.woff'
BASE_FONT = {
    'uniEA64': '0',
    'uniF0A1': '1',
    'uniF662': '2',
    'uniF8B2': '3',
    'uniF69D': '4',
    'uniE450': '5',
    'uniF442': '6',
    'uniE2AE': '7',
    'uniE90F': '8',
    'uniE7B8': '9',
}

# 初始化字体文件目录
font_dir = os.path.join(os.path.curdir, 'fonts')
if not os.path.isdir(font_dir):
    os.mkdir(font_dir)

# 创建处理basefont字体文件的对象
basefont = TTFont(BASE_FONT_PATH)
hex2num = {basefont['glyf'][i].coordinates.array.tobytes().hex():BASE_FONT[i]
           for i in basefont.getGlyphOrder()[2:]}
# pprint(hex2num)

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }

r = requests.get('http://maoyan.com/films/1229020', headers=headers)
selector = parsel.Selector(r.text)
# 解析出字体文件的URL
woff = selector.re_first("url\('(.+?\.woff)'\)")
# 确定字体文件下载后保存的路径
download_font_path = os.path.join('./fonts', os.path.basename(woff))
if not os.path.isfile(download_font_path):
    urllib.request.urlretrieve('http:%s' % woff, download_font_path)

# 创建当前页面使用的这套字体文件的对象
font = TTFont(download_font_path)
# 根据当前页面的字体文件生成{字体编码：字符编码}的对应关系
hex2u = {font['glyf'][i].coordinates.array.tobytes().hex():i for i in font.getGlyphOrder()[2:]}
# pprint(hex2u)

# Unicode字符和数字之间的对应关系
u2num = {}
for h, u in hex2u.items():
    u2num[u] = hex2num[h]
# 小数点单独处理一下
u2num['uni2E'] = '.'
# pprint(u2num)

# 接下来就可以正常解析数据了
box = selector.xpath('//div[contains(@class, "box")]')
box_num = box.xpath('./span[@class="stonefont"]/text()').get()
box_unit = box.xpath('./span[@class="unit"]/text()').get()
t = lambda x: 'uni' + '%x'.upper() % ord(x)
box_num = ''.join([u2num[t(i)] for i in box_num])
print('%s%s' % (box_num, box_unit))