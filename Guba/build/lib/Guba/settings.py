# -*- coding: utf-8 -*-

# Scrapy settings for Guba project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Guba'

SPIDER_MODULES = ['Guba.spiders']
NEWSPIDER_MODULE = 'Guba.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# scrapy-redis
# REDIS_URL = 'redis://:yzd@127.0.0.1:6379'  # for master
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
REDIS_HOST = '120.***.***.***'  # 也可以根据情况改成 localhost
REDIS_PORT = 6379
REDIS_URL = None
REDIS_PARAMS = {'password': '*******'}

CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 32
CONCURRENT_REQUESTS_PER_IP = 32

MYSQL_HOST = '123.***.***.***'
MYSQL_DBNAME = 'Guba'
MYSQL_USER = 'root'
MYSQL_PASSWD = '*******'
COOKIES_ENABLED = False


DOWNLOAD_DELAY = 0.3

LOG_LEVEL = 'INFO'

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None
 }


ITEM_PIPELINES = {
    'Guba.pipelines.GubaPipeline': 300,
}


DOWNLOADER_MIDDLEWARES = {
   'Guba.middlewares.RandomUserAgentMiddleware': 543,
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
