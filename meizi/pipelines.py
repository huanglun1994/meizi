# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem
import os
import re


def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[/\\:*?"<>|]', '', str(path))
    return path


class MeiziPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        """
        :param request: 每一个图片下载管道请求
        :param response:
        :param info:
        :param strip :清洗Windows系统的文件夹非法字符，避免无法创建目录
        :return: 每套图的分类目录
        """
        item = request.meta['item']
        folder = item['tags']
        folder_strip = strip(folder)
        image_name = '-'.join(request.url.split('/')[-3:])
        image_path = u'full/{0}/{1}'.format(folder_strip, image_name)
        return image_path

    def get_media_requests(self, item, info):
        """
        :param item: meizi.py中返回的item 
        :param info: 
        :return: 
        """
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'item': item})

    def process_item(self, item, spider):
        fold_name = item['tags']  # 图片文件夹名，以图片标签分类
        images = []
        dir_path = '%s/%s' % (settings.IMAGES_STORE, fold_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for image_url in item['image_urls']:
            image_name = '-'.join(image_url.split('/')[-3:])  # 图片名
            image_path = '%s/%s' % (dir_path, image_name)
            images.append(image_path)

            with open(image_path, 'wb') as f:
                res = requests.get(image_url)
                f.write(res.content)
        item['images'] = images
        return item
