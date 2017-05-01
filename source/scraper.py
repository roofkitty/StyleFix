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

def get_images(info, path):
    """
    Get images
    """
    regx = r'src="(.*?.jpg)" '
    pat = re.compile(regx)
    images_code = re.findall(pat, info)
    i = 0
    for image_url in images_code:
        urllib.urlretrieve(image_url, '%s.jpg' % i)
        i += 1

def scraper(url, path):
    info = get_content(url)
    get_images(info, path)

if __name__ == '__main__':
    url = sys.argv[1]
    path = sys.argv[2]

    scraper(url, path)

