# -*- coding: utf-8 -*-
"""xxxxx"""
__author__ = 'Huang Lun'
import scrapy
from scrapy.selector import Selector
from meizi.items import MeiziItem


class MeiziSpider(scrapy.Spider):
    name = 'meizi'  # 爬虫名，name是必要参数
    allowed_domains = ['http://www.meizitu.com/a/']  # 爬虫的爬取范围
    start_urls = ['http://www.meizitu.com/a/more_1.html']  # 爬虫的起始网址

    def parse(self, response):
        sel = Selector(response)
        # 使用xpath选择器进行标签选择，也可以使用css选择器
        # 链接到图片详情页面
        for link in sel.xpath("//h3[@class='tit']/a/@href").extract():
            request = scrapy.Request(link, callback=self.parse_image)
            yield request
        #for link in sel.css("h3.tit a::attr(href)").extract():
        #    request = scrapy.Request(link, callback=self.parse_image)
        #    yield request

        # 连接到下一页，此处需使用css选择器，xpath暂未找到选择下一兄弟节点的方法
        next_page = response.css('div#wp_page_numbers ul li.thisclass + li a::attr(href)').extract_first()
        if next_page is not None:
            request_next = scrapy.Request('http://www.meizitu.com/a/%s' % next_page, self.parse)
            yield request_next

    def parse_image(self, response):
        """将选取的节点传入Item对应的数据项中"""
        item = MeiziItem()
        sel = Selector(response)

        tags = sel.xpath("//meta[@name='keywords']/@content").extract()
        #tags = sel.css("meta[name='keywords']::attr(content)").extract()
        image_urls = sel.xpath("//div[@id='picture']/p/img/@src").extract()
        #image_urls = sel.css("div#picture p img::attr(src)").extract()

        item['tags'] = tags
        item['image_urls'] = image_urls
        yield item
