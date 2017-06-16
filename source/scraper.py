"""
Provide API to scraping pictures from given URL
"""
import urllib
import re
import sys

def get_content(url):
    """
    For a given url, download content
    """
    html = urllib.urlopen(url)
    content = html.read()
    html.close()
    return content

def get_images(page_content, path):
    """
    Get images on a page, and store to location specified by path
    """
    regx = r'src="(.*?.jpg)" '
    pattern = re.compile(regx)
    images_code = re.findall(pattern, page_content)
    i = 0
    for image_url in images_code:
        urllib.urlretrieve(image_url, '%s.jpg' % i)
        i += 1

def scraper(url, path):
    """
    Download images on the page at the url, to location specified by path
    """
    page_content = get_content(url)
    get_images(page_content, path)

if __name__ == '__main__':
    url_page = sys.argv[1]
    path_store = sys.argv[2]

    scraper(url_page, path_store)

