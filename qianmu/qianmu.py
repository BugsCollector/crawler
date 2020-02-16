import sys
import requests
from lxml import html

resp = requests.get('http://www.qianmu.org/ranking/1528.htm')
selector = html.etree.HTML(resp.text)
links = selector.xpath('//div[@class="rankItem"]//td[2]//a//@href')
for link in links:
    if link.startswith('http://qianmu.org'):
        link += 'http://qianmu.org/'
    r = requests.get(link)
    sel = html.etree.HTML(r.text)
    university = {}
    university['name'] = sel.xpath('//div[@id="wikiContent"]/h1/text()')[0].strip()
    keys = sel.xpath('//div[@id="wikiContent"]/div[@class="infobox"]//table//td[1]/p/text()')
    cols = sel.xpath('//div[@id="wikiContent"]/div[@class="infobox"]//table//td[2]')
    values = [' '.join(col.xpath('.//text()')) for col in cols]
    if len(keys) != len(values):
        continue

    university.update(zip(keys, values))
    sys.exit(0)
