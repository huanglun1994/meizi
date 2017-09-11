# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeiziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tags = scrapy.Field()  # 图片标签
    image_urls = scrapy.Field()  # 图片地址
    images = scrapy.Field()  # 图片
