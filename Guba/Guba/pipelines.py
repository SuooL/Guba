# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from Guba import settings
from Guba.items import UsersItem
from Guba.items import GubaItem
from Guba.items import NewsItem
from Guba.items import StockBarItem
from Guba.items import CommentsItem
import logging
logger = logging.getLogger(__name__)


class GubaPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.place_holder = ""
        self.select_key = ""
        self.params = []
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.place_holder = ""
        self.select_key = ""
        self.params = []

        sql = ""
        item_type = ""
        field_key = ""
        if isinstance(item, GubaItem):
            sql = "REPLACE INTO Companys("
            field_key = "name"
            item_type = "Companys"
        elif isinstance(item, UsersItem):
            sql = "REPLACE INTO Users("
            field_key = "user_nickname"
            item_type = "Users"
        elif isinstance(item, NewsItem):
            sql = "REPLACE INTO News("
            field_key = "title"
            item_type = "News"
        elif isinstance(item, CommentsItem):
            sql = "REPLACE INTO Comments("
            field_key = "news_id"
            item_type = "Comments"
        elif isinstance(item, StockBarItem):
            sql = "REPLACE INTO Gubas("
            field_key = "stockbar_name"
            item_type = "StockBarItem"

        for key, values in item.items():
            if self.select_key != "":
                self.select_key += ","
            self.select_key += key
            if self.place_holder != "":
                self.place_holder += ","
            self.place_holder += "%s"
            self.params.append(values)
        sql += self.select_key + ") VALUES(" + self.place_holder + ")"

        try:
            self.cursor.execute(sql, self.params)
            self.connect.commit()
        except Exception as e:
            print(e)
            log = "%s %s 存储出错" % (item_type, item[field_key])
            logger.error(log)
            print(log)
            with open('save_list.txt', 'a+') as wf:
                wf.write(log + '\n')
            pass
        return item

    def close_spider(self, spider):
        self.connect.close()


