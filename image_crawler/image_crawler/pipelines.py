# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""
Item pipeline components.
"""
import json

class DuplicatesPipeline(object):
    """
    Item pipeline component to drop duplicate image urls.
    """
    def __init__(self):
        self.image_urls_seen = set()

    def process_item(self, item, spider):
        """
        Update image_urls by removing urls that are already seen.
        """
        item['image_urls'].difference_update(self.image_urls_seen)

        self.image_urls_seen = self.image_urls_seen.union(item['image_urls'])

        return item

def setToList(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

class OutputJsonPipeline(object):
    """
    Item pipeline component to write the resulting image urls to a JSON file.
    """

    def open_spider(self, spider):
        self.image_urls_dict = dict() # mapping blog id to a list of image urls on that blog

    def close_spider(self, spider):
        with open('../output/image_urls.json', 'w') as output:
            json.dump(self.image_urls_dict, output, default=setToList)

    def process_item(self, item, spider):
        if item['blog_id'] in self.image_urls_dict:
            existing_items = self.image_urls_dict[item['blog_id']]
            self.image_urls_dict[item['blog_id']] = existing_items.union(item['image_urls'])
        else:
            self.image_urls_dict[item['blog_id']] = item['image_urls']

        return item

