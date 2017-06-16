"""
The Scrapy spider for crawling blogs.
"""
import csv
import scrapy

class ImagesSpider(scrapy.Spider):
    """
    The spider for crawling image urls and saving them locally.
    """
    name = "images"

    def start_requests(self):
        """
        Reads from input/bloggers.csv and send a scrapy.Request for each home page.
        Writes a mapping of blog identifier to image urls to /output.
        """
        with open('../input/bloggers_debug.csv', 'r') as bloggers_csv:
            reader = csv.reader(bloggers_csv)
            next(reader) # skip header row
            for row in reader:
                blog_id = row[0]
                yield scrapy.Request(url=row[1], callback=self.parse, meta={'blog': blog_id})

    def parse(self, response):
        blog_id = response.meta.get('blog')
        # dedupe all image urls on one page
        image_urls_on_page = set(response.css('img').re(r'src="(.*?.jpg)"'))
        yield {
            'blog_id': blog_id,
            'image_urls': image_urls_on_page
        }

        linked_page = response.css('li a::attr("href")').extract()
        if linked_page is not None:
            for page in linked_page:
                if not any(x in page for x in ('customer', 'account', 'checkout', 'cart', 'forgotpassword', 'catalog')):
                    print('LINKED PAGE')
                    print(page)
                    print('')
                    yield response.follow(url=page, callback=self.parse, meta={'blog': blog_id})
