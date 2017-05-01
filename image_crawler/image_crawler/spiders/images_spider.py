"""
A crawler
"""
import csv
import scrapy

class ImagesSpider(scrapy.Spider):
    """
    The spider for crawling image urls and saving them locally
    """
    name = "images"

    def start_requests(self):
        """
        Read from input/bloggers.csv and send a scrapy.Request for each home page
        """
        with open("../input/bloggers_debug.csv", 'r') as bloggers_csv:
            reader = csv.reader(bloggers_csv)
            next(reader) # skip header row
            for row in reader:
                yield scrapy.Request(url=row[1], callback=self.parse, meta={'blog': row[0]})

    def parse(self, response):
        print '------- in parse callback, logging blog name:' + response.meta.get('blog')
        for image_url in response.css('img').re(r'src="(.*?.jpg)"'):
            yield {
                'url': image_url
            }


    # def parse_image_urls(self, response):
    #     pass

    # def save_images(self, url):
    #     pass
