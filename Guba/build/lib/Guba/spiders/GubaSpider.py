# -*- coding: utf-8 -*-
import scrapy
import re
import logging
from Guba.items import GubaItem
logger = logging.getLogger(__name__)


class GubaSpider(scrapy.Spider):
    name = 'GubaSpider'
    allowed_domains = ['guba.eastmoney.com']
    start_urls = ['http://guba.eastmoney.com/remenba.aspx?type=1&tab=6']

    def parse(self, response):
        company = GubaItem()

        all_list = response.xpath("//*[contains(@class, 'ngblistul2')]/li/a")

        for item in all_list:

            href = item.xpath(".//@href").extract_first()
            company['url'] = 'http://guba.eastmoney.com/{link}'.format(link=href)
            info = item.xpath(".//text()").extract_first().split(")")
            company['code'] = info[0].replace('(', '').strip()   #re.findall(r'(\d+)', info[0])
            company['name'] = info[1].strip()
            company['type'] = '三板'
            # print("{code}:{name}".format(code=company['code'], name=company['name']))

            yield company

        all_list_hide = response.xpath("//*[contains(@class, 'ngblistul2 hide')]/li/a")

        for item in all_list_hide:
            href = item.xpath(".//@href").extract_first()
            company['url'] = 'http://guba.eastmoney.com/{link}'.format(link=href)
            info = item.xpath(".//text()").extract_first().split(")")
            company['code'] = info[0].replace('(', '').strip() #re.findall(r'(\d+)', info[0])
            company['name'] = info[1].strip()
            company['type'] = '三板'
            # print("{code}:{name}".format(code=company['code'], name=company['name']))

            yield company
