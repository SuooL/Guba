# -*- coding: utf-8 -*-
# import scrapy
from scrapy_redis.spiders import RedisSpider
from Guba.items import NewsItem
import re
import redis


class NewsItemUrlSpider(RedisSpider):
    name = 'NewsItemUrlSpider'
    allowed_domains = ['guba.eastmoney.com']
    redis_key = 'News:start_urls'

    def parse(self, response):

        # redis_connect = redis.Redis(host='120.***.***.***', port=6379, db=0, password='*******')
        redis_connect = redis.Redis(host='localhost', port=6379, db=0)

        host = "http://guba.eastmoney.com"

        if "Error" in response.url:
            print("%s 错误的地址" % response.url)
            with open('wrong_list.txt', 'a+') as wf:
                wf.write("%s\n" % response.url)
        else:
            print(response.url)
            all_list = response.xpath("//*[contains(@class, 'articleh normal_post')]")
            for newsItem in all_list:
                news = NewsItem()
                title = newsItem.xpath(".//span[@class='l3 a3']/a/@title").extract_first()
                suffix = newsItem.xpath(".//span[@class='l3 a3']/a/@href").extract_first().strip()
                company_code = re.findall(r",(\d+),", suffix)
                news_id = re.findall(r",(\d+)\.", suffix)
                linkurl = host + suffix
                news['title'] = title
                news['news_id'] = news_id
                news['company_code'] = company_code
                news['linkurl'] = linkurl
                redis_connect.sadd('NewsContent:start_urls', linkurl)
                yield news
