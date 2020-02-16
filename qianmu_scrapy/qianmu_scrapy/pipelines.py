# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class QianmuScrapyPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='qianmu',
            user='root',
            password='lhj@CZ2009',
            charset='utf8',
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        # keys = item.keys()
        # values = [item[k] for k in keys]
        keys, values = zip(*item.items())
        tmp_k = []
        for k in keys:
            tmp_k.append('`'+ k +'`')
        keys = ','.join(tmp_k)
        sql = 'insert into universities (%s) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' %(keys,
            values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])

        self.cur.execute(sql)
        self.conn.commit()
        # print(self.cur._last_executed)
        return item
