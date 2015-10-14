# -*- coding: utf-8 -*-
__author__ = 'PGY'
import timeit
start = timeit.default_timer()

import requests
import re
from bs4 import BeautifulSoup, SoupStrainer

def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    images_and_info = SoupStrainer(['div', {'class': 'img01'}, 'script', {'type': 'text/javascript'}])
    soup = BeautifulSoup(plain_text, "html.parser", parse_only=images_and_info)
    all_imgs = soup.find_all('img', {'src': re.compile('.+'), 'name': 'ImgList'})
    imglist = []
    for img in all_imgs:
        imglink = img.get('src')
        imglist.append(imglink)
    allinfo = soup.find('script').get_text()
    roominfo = allinfo.split('var')[1]
    roominfolist = roominfo.replace(' ','').replace(',','').replace('\'','').split('\r\n')[1:-3]
    roominfolistnew = [infoitem.split(":") for infoitem in roominfolist]
    roominfodict = dict(roominfolistnew)
    return (imglist, roominfodict)

def get_rooms(max_pages):
    page = 1
    allimginfolist = []
    while page <= max_pages:
        url = "http://zu.fang.com/house/"
        url = url + "i3" + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        titles = SoupStrainer('p',{'class': 'title'})
        soup = BeautifulSoup(plain_text, "html.parser", parse_only=titles)
        all_a_tag = soup.find_all('a', {'href': re.compile('.+')})
        all_a_tag.pop()
        for link in all_a_tag:
            href = "http://zu.fang.com" + link.get('href')
            print(href)
            imginfotuple = get_single_item_data(href)
            allimginfolist.append(imginfotuple)
        page = page + 1
    return allimginfolist
result = get_rooms(3)
print(result)

stop = timeit.default_timer()

print(stop - start)
