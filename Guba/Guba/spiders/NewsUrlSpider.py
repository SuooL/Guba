# -*- coding: utf-8 -*-
# import scrapy
from scrapy_redis.spiders import RedisSpider
from Guba.items import NewsItem
import re
import redis
import math


total = 1522
count = 1


class NewsSpider(RedisSpider):
    name = 'NewsUrlSpider'
    allowed_domains = ['guba.eastmoney.com']
    redis_key = 'Guba:start_urls'

    def parse(self, response):
        global count, total

        if count % 50 == 0:
            print("已经爬取了 %d 个页面，完成比例是 %.2f" % (count, count/total))
        # global redis_connect
        redis_connect = redis.Redis(host='120.***.***.***', port=6379, db=0, password='*******')
        # news = NewsItem()
        # host = "http://guba.eastmoney.com"

        if "Error" in response.url:
            print("%s 错误的地址" % response.url)
            with open('wrong_list.txt', 'a+') as wf:
                wf.write("%s\n" % response.url)
        else:
            print(response.url)
            code = response.url.split(",")

            if len(code) >= 2:
                code = code[1]
                # all_list = response.xpath("//*[contains(@class, 'articleh normal_post')]")
                page_num = response.xpath(".//*[contains(@class, 'pagernums')]/@data-pager")
                if page_num is not None and len(page_num) > 0:
                    page_num = page_num.extract_first().split("|")[-3:]
                    news_num = int(page_num[0])
                    segment_num = int(page_num[1])
                    page = math.ceil(news_num / segment_num)
                    print("{code}共有{page}页".format(code=code, page=page))
                    for index in range(1, page + 1):
                        news_url = "http://guba.eastmoney.com/list,{code},1,f_{page}.html".format(code=code, page=index)
                        # print(news_url)
                        redis_connect.rpush('News:start_urls', news_url)
                else:
                    print("%s 近一年内没有新闻资讯" % code)
                    with open('no_news_list.txt', 'a+') as wf:
                        wf.write("%s\n" % code)
            count += 1
        # for newsItem in all_list:
        #     title = newsItem.xpath(".//span[@class='l3 a3']/a/@title").extract_first()
        #     suffix = newsItem.xpath(".//span[@class='l3 a3']/a/@href").extract_first().strip()
        #     company_code = re.findall(r",(\d+),", suffix)
        #     news_id = re.findall(r",(\d+)\.", suffix)
        #     linkurl = host + suffix
        #     news['title'] = title
        #     news['news_id'] = news_id
        #     news['company_code'] = company_code
        #     news['linkurl'] = linkurl
        #
        #
        # yield news
