# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
from meizi import settings
import os


class MeiziPipeline(object):
    def process_item(self, item, spider):
        fold_name = item['tags']
        images = []
        dir_path = '%s/%s' % (settings.IMAGES_STORE, fold_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for image_url in item['image_urls']:
            image_name = '-'.join(image_url.split('/')[-3:])
            image_path = '%s/%s' % (dir_path, image_name)
            images.append(image_path)

            with open(image_path, 'wb') as f:
                res = requests.get(image_url)
                f.write(res.content)
        item['images'] = images
        return item
