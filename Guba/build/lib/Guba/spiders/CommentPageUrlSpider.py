# -*- coding: utf-8 -*-
# import scrapy
from scrapy_redis.spiders import RedisSpider
from Guba.items import NewsItem
from Guba.items import UsersItem
from Guba.items import StockBarItem
from Guba.items import CommentsItem
import re
import math
import redis
import json
import logging
logger = logging.getLogger(__name__)


class CommentPageUrlSpider(RedisSpider):
    name = 'CommentPageUrlSpider'
    allowed_domains = ['guba.eastmoney.com']
    redis_key = 'NewsContent:start_urls' #'NewsContent:start_urls'

    def parse(self, response):
        #pool = redis.ConnectionPool(host='localhost', port=6379, password='*******', decode_responses=True)
        pool = redis.ConnectionPool(host='120.***.***.***', port=6379, db=0, password='*******', \
                                     decode_responses=True)
        redis_connect = redis.Redis(connection_pool=pool)

        def generate_url(comment_count, code, post_id):
            page = math.ceil(comment_count / 30)
            for index in range(2, page + 1):
                url = 'http://guba.eastmoney.com/news,{code},{post}_{page}.html#storeply'. \
                    format(code=code, post=post_id, page=index)
                redis_connect.sadd("NewsCommentUrl_bkp:start_urls", url)

        # code redis bar和user只要查一次

        if "Error" in response.url:
            print("%s 错误的地址" % response.url)
            with open('wrong_list.txt', 'a+') as wf:
                wf.write("%s\n" % response.url)
        else:
            # generate_without_comment()
            com_code = re.findall(r',(\S+),', response.url)[0]
            news = NewsItem()
            author_user = UsersItem()
            bar = StockBarItem()
            try:
                post_article = json.loads(re.findall('var post_article =(.*);', response.text)[0])
                if post_article is not None and len(post_article.keys()) > 0:
                    author_user_j = post_article['post']['post_user']
                    bar_j = post_article['post']['post_guba']
                    post_j = post_article['post']

                    for key_u in author_user_j:
                        author_user[key_u] = author_user_j[key_u]
                    for key_b in bar_j:
                        bar[key_b] = bar_j[key_b]

                    news['news_id'] = post_j['post_id']
                    news['title'] = post_j['post_title']
                    news['post_click_count'] = post_j['post_click_count']
                    news['post_comment_count'] = post_j['post_comment_count']
                    news['post_forward_count'] = post_j['post_forward_count']
                    news['post_like_count'] = post_j['post_like_count']
                    news['post_publish_time'] = post_j['post_publish_time']
                    news['linkurl'] = response.url
                    source = response.xpath("//*[contains(@class, 'source')]/text()").extract_first()
                    if source is not None and len(source) > 0:
                        news['source'] = source.split('：')[-1]
                    else:
                        source = response.xpath("//div[@id='zw_header']/text()").extract_first()
                        if source is not None and len(source) > 0:
                            news['source'] = '___'.join(source.split('：'))
                        else:
                            news['source'] = 'UNKNOW'
                    news['post_source_id'] = post_j['post_source_id']
                    if author_user_j is not None and len(author_user_j.keys()) > 0:
                        news['author_id'] = author_user_j['user_id']
                    if bar_j is not None and len(bar_j.keys()) > 0:
                        news['company_code'] = bar_j['stockbar_code']
                    if 'company_code' in news.keys() and 'news_id' in news.keys():
                        generate_url(int(post_j['post_comment_count']), news['company_code'], news['news_id'])
                    else:
                        news_code = re.findall(r',(\S+)\.', response.url)[0]
                        generate_url(int(post_j['post_comment_count']), com_code, news_code)
                    if not redis_connect.sismember('company_code', com_code):
                        redis_connect.sadd('company_code', com_code)
                        yield author_user
                        yield bar
                    yield news
                else:
                    logger.error("%s json 解析为空" % response.url)
                    with open('json_error_list.txt', 'a+') as wf:
                        wf.write("%s json 解析为空\n" % response.url)
            except Exception as e:
                logger.error("%s json 解析出错, 错误原因 %s" % (response.url, e))
                with open('json_error_list.txt', 'a+') as wf:
                    wf.write("%s json 解析出错, 错误原因 %s \n" % (response.url, e))

            comments_list = response.xpath('.//div[@id="zwlist"]/*[contains(@class, "zwli clearfix")]')

            if comments_list is not None and len(comments_list) > 0:
                for comm in comments_list:
                    comment_user = UsersItem()
                    comment = CommentsItem()
                    try:
                        user_j = json.loads(comm.xpath('.//div[@class="data"]/@data-json').extract_first())
                        for key in user_j:
                            comment_user[key] = user_j[key]
                        comment['comment_id'] = comm.xpath('.//@data-huifuid').extract_first()
                        comment['user_id'] = comment_user['user_id']
                        comment['news_id'] = re.findall(r',(\d+)\.', response.url)[0]
                        pub_time = comm.xpath('.//*[contains(@class, "zwlitime")]/text()').extract_first().\
                            replace('\r', '').replace('\n', '').strip()
                        comment['post_time'] = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})", pub_time)

                        comment['content'] = ''.join(comm.xpath('.//*[contains(@class, "short_text")]/text()').extract()).\
                            replace('\r', '').replace('\n', '').strip()
                        comment['like_count'] = comm. xpath('.//@data-reply_like_count').extract_first()
                        yield comment
                        if not redis_connect.sismember('user_code', comment_user['user_id']):
                            redis_connect.sadd('user_code', comment_user['user_id'])
                            yield comment_user
                    except Exception as e:
                        logger.error("评论部分用户 %s json 解析出错, 错误原因 %s \n" % (response.url, e))
                        with open('json_c_user_error_list.txt', 'a+') as wf:
                            wf.write("评论部分用户 %s json 解析出错, 错误原因 %s \n" % (comm.extract(), e))
