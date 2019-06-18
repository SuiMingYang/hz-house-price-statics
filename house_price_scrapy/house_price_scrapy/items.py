# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HousePriceScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    longitude = scrapy.Field() #经度
    latitude = scrapy.Field() #纬度
    estate_name = scrapy.Field() #小区名
    date = scrapy.Field() #日期
    price = scrapy.Field() #价格
    sales_count = scrapy.Field() #销量
    sales = scrapy.Field() #板块评级
    sales = scrapy.Field() #物业评级
    sales = scrapy.Field() #活跃度评级
    sales = scrapy.Field() #教育评级
    sales = scrapy.Field() #搜索热度


