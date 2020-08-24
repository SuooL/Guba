# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class GubaItem(scrapy.Item):
    # define the fields for your item here like:
    code = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()


class StockBarItem(scrapy.Item):
    # define the fields for your item here like:
    stockbar_type = scrapy.Field()
    stockbar_code = scrapy.Field()
    stockbar_inner_code = scrapy.Field()
    stockbar_name = scrapy.Field()
    stockbar_market = scrapy.Field()
    stockbar_quote = scrapy.Field()
    stockbar_exchange = scrapy.Field()
    stockbar_external_code = scrapy.Field()


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    news_id = scrapy.Field()
    title = scrapy.Field()
    post_click_count = scrapy.Field()
    post_comment_count = scrapy.Field()
    post_forward_count = scrapy.Field()
    post_like_count = scrapy.Field()
    post_publish_time = scrapy.Field()
    linkurl = scrapy.Field()
    source = scrapy.Field()
    post_source_id = scrapy.Field()
    author_id = scrapy.Field()
    company_code = scrapy.Field()


class GubaSpiderLoader(ItemLoader):
    default_item_class = NewsItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()


class UsersItem(scrapy.Item):
    user_id = scrapy.Field()
    user_nickname = scrapy.Field()
    user_age = scrapy.Field()
    user_avatar = scrapy.Field()
    user_name = scrapy.Field()
    user_v = scrapy.Field()
    user_type = scrapy.Field()
    user_is_majia = scrapy.Field()
    user_level = scrapy.Field()
    user_first_en_name = scrapy.Field()
    user_influ_level = scrapy.Field()
    user_black_type = scrapy.Field()
    user_bizflag = scrapy.Field()
    user_bizsubflag = scrapy.Field()
    user_extend = scrapy.Field()
    user_introduce = scrapy.Field()


class CommentsItem(scrapy.Item):
    # define the fields for your item here like:
    comment_id = scrapy.Field()
    user_id = scrapy.Field()
    news_id = scrapy.Field()
    post_time = scrapy.Field()
    content = scrapy.Field()
    like_count = scrapy.Field()
