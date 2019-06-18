# -*- coding: utf-8 -*-
import scrapy
from house_price_scrapy.items import HousePriceScrapyItem
from urllib import parse
from scrapy import Spider, Request, cmdline

class HouseSpiderSpider(scrapy.Spider):
    name = 'house_spider'
    allowed_domains = ['fangjia.fang.com']
    start_urls = ['http://fangjia.fang.com/']

    def parse(self, response):
        pass
    
    def parse_block(self, response):
        city_list = response.xpath('//*[@id="main"]/div/div[2]/ul/li')
        item = ()
        for city_detail in city_list:
            # 依次遍历城市URL
            info_primary=city_detail.xpath('.//div/div[1]')
            info_company=city_detail.xpath('.//div/div[2]')
            info_publis=city_detail.xpath('.//div/div[3]')
            # 解析每个城市的月份数据
            request = scrapy.Request(city_detail_url, callback=self.parse_detail)
            
            yield request

    def parse_detail(self, response):
        city_list = response.xpath('//*[@id="main"]/div/div[2]/ul/li')
        item = HousePriceScrapyItem()
        for city_detail in city_list:
            # 依次遍历城市URL
            info_primary=city_detail.xpath('.//div/div[1]')
            info_company=city_detail.xpath('.//div/div[2]')
            info_publis=city_detail.xpath('.//div/div[3]')
            # 解析每个城市的月份数据
            item['cityname'] = info_primary.xpath('.//p/text()').extract()[0].split(" ")[0].strip()
            item['company'] = info_company.xpath('.//div/h3/a/text()').extract_first() 
            item['experience'] =  info_primary.xpath('.//p/text()').extract()[1]
            item['education'] = info_primary.xpath('.//p/text()').extract()[2] #if len(info_primary.xpath('.//p/text()').extract())==3 else ""
            item['salary'] = info_primary.xpath('.//h3/a/span/text()').extract_first() 
            item['company_size'] = info_company.xpath('.//div/p/text()').extract()[2] if len(info_company.xpath('.//div/p/text()').extract())==3 else ""
            item['industry'] = info_company.xpath('.//div/p/text()').extract()[0]
            item['recruiter'] = info_publis.xpath('.//h3/text()').extract_first() 
            item['publishdate'] = info_publis.xpath('.//p/text()').extract_first() 

            print(item)
            yield item