import threading
from queue import Queue
import time
import sys
import requests
from lxml import html

link_queue = Queue()
threads_num = 10
threads = []
download_pages = 0

def parse_university(link):
    r = requests.get(link)
    global download_pages
    download_pages += 1
    sel = html.etree.HTML(r.text)
    university = {}
    university['name'] = sel.xpath('//div[@id="wikiContent"]/h1/text()')[0].strip()
    keys = sel.xpath('//div[@id="wikiContent"]/div[@class="infobox"]//table//td[1]/p/text()')
    cols = sel.xpath('//div[@id="wikiContent"]/div[@class="infobox"]//table//td[2]')
    values = [' '.join(col.xpath('.//text()')) for col in cols]
    if len(keys) != len(values):
        return

    university.update(zip(keys, values))

def download():
    while True:
        link = link_queue.get()
        if link:
            parse_university(link)
            link_queue.task_done()
            print('remaining queue: %s' % link_queue.qsize())
        else:
            break


if __name__ == '__main__':
    start_time = time.time()
    resp = requests.get('http://www.qianmu.org/ranking/1528.htm')
    selector = html.etree.HTML(resp.text)
    links = selector.xpath('//div[@class="rankItem"]//td[2]//a//@href')
    for link in links:
        if link.startswith('http://qianmu.org'):
            link += 'http://qianmu.org/'
        link_queue.put(link)

    for i in range(threads_num):
        t = threading.Thread(target=download)
        t.start()
        threads.append(t)
    link_queue.join()

    for i in range(threads_num):
        link_queue.put(None)

    for t in threads:
        t.join()

    cost = time.time() - start_time
    print('download %s pages, cost %s secs' % (download_pages, cost))
