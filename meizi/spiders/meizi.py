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
        # 链接到图片详情页面，调用parse_image
        links = sel.xpath("//h3[@class='tit']/a/@href").extract()
        if links:
            for link in links:
                yield scrapy.Request(link, callback=self.parse_image)
        # links = sel.css("h3.tit a::attr(href)").extract()

        # 连接到下一页，此处需使用css选择器，xpath暂未找到选择下一兄弟节点的方法
        next_page = response.css('div#wp_page_numbers ul li.thisclass + li a::attr(href)').extract_first()

        # 如果有下一页，则回调parse
        if next_page:
            yield scrapy.Request('http://www.meizitu.com/a/%s' % next_page, callback=self.parse)

    def parse_image(self, response):
        """
        将数据传入item
        :param response: 
        :return: 
        """
        item = MeiziItem()
        sel = Selector(response)

        tags = sel.xpath("//meta[@name='keywords']/@content").extract_first().strip()  # 图片标签
        # tags = sel.css("meta[name='keywords']::attr(content)").extract().strip()
        image_urls = sel.xpath("//div[@id='picture']/p/img/@src").extract()  # 图片链接
        # image_urls = sel.css("div#picture p img::attr(src)").extract()

        # 将tags，image_urls存入item中
        item['tags'] = tags
        item['image_urls'] = image_urls
        yield item
