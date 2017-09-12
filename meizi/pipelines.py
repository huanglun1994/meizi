# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
import re
import os
from meizi.settings import IMAGES_STORE


def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[/\\:*?"<>|]', '', str(path))  # Windows的文件名非法字符有：/\\:*?"<>|
    return path


class MeiziPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'item': item})  # 传入item，分类文件夹时需要用到

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images')
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = '_'.join(request.url.split('/')[-3:])  # 图片的保存名
        fold_name = strip(item['tags'].strip())  # 文件夹名
        fold_path = u'{0}/{1}'.format(IMAGES_STORE, fold_name)  # 完整路径
        if not os.path.exists(fold_path):
            os.makedirs(fold_path)
        filename = u'{0}/{1}'.format(fold_path, image_guid)
        return filename
