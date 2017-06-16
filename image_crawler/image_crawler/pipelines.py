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
    Item pipeline component to drop duplicate image urls and also image urls
    containing certain keywords
    """
    def __init__(self):
        self.image_urls_seen = set()

    def process_item(self, item, spider):
        """
        Update image_urls by removing urls that are already seen.
        """
        item['image_urls'].difference_update(self.image_urls_seen)

        self.image_urls_seen = self.image_urls_seen.union(item['image_urls'])

        # TODO ignore all image_url with 'catalog' in it before going to the download pipeline

        return item

def setToList(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

class OutputJsonPipeline(object):
    """
    Item pipeline component to write the resulting image urls and stored file path to a JSON file.
    The image url and stored path information are in the 'images' field of item
    """

    def open_spider(self, spider):
        self.image_urls_dict = dict() # mapping blog id to a list of image urls on that blog

    def close_spider(self, spider):
        with open('../output/images_info.json', 'w') as output:
            json.dump(self.image_urls_dict, output, default=setToList)

    def process_item(self, item, spider):
        blog_id = item['blog_id']
        if blog_id in self.image_urls_dict:
            self.image_urls_dict[blog_id].extend(item['images'])
        else:
            if item['images']:
                self.image_urls_dict[blog_id] = item['images']
        return item
