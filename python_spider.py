# -*- coding: utf-8 -*-
__author__ = 'PGY'
import timeit
start = timeit.default_timer()
from threading import Thread
import requests
import re
from bs4 import BeautifulSoup, SoupStrainer

def get_single_item_data(item_url):
    '''function to get the room images and info in each page'''
    # get the page source and parse the code
    source_code = requests.get(item_url)
    plain_text = source_code.text
    images_and_info = SoupStrainer(['div', {'class': 'img01'}, 'script', {'type': 'text/javascript'}])
    soup = BeautifulSoup(plain_text, "html.parser", parse_only=images_and_info)
    # get all the links for the images
    all_imgs = soup.find_all('img', {'src': re.compile('.+'), 'name': 'ImgList'})
    imglist = []
    for img in all_imgs:
        imglink = img.get('src')
        imglist.append(imglink)
    # get the room information
    allinfo = soup.find('script').get_text()
    roominfo = allinfo.split('var')[1]
    # process the data to save the roominfo properly in dictionary data structure
    roominfolist = roominfo.replace(' ','').replace(',','').replace('\'','').split('\r\n')[1:-3]
    roominfolistnew = [infoitem.split(":") for infoitem in roominfolist]
    roominfodict = dict(roominfolistnew)
    print(imglist)
    return (imglist, roominfodict)

def get_rooms(page):
    '''function to get all the room information with specified page number'''
    allimginfolist = []
    url = "http://zu.fang.com/house/"
    url = url + "i3" + str(page)
    source_code = requests.get(url)
    plain_text = source_code.text
    titles = SoupStrainer('p',{'class': 'title'})
    soup = BeautifulSoup(plain_text, "html.parser", parse_only=titles)
    all_a_tag = soup.find_all('a', {'href': re.compile('.+')})
    all_a_tag.pop()
    # for each link, spide into the link and get room info and all images
    for link in all_a_tag:
        href = "http://zu.fang.com" + link.get('href')
        #print(href)
        imginfotuple = get_single_item_data(href)
        allimginfolist.append(imginfotuple)
    return allimginfolist

# iterate through all pages and create thread for each page and append each thread to the infolist
infolist = []
for i in range(3):
    thread_page = Thread(target=get_rooms, args=(i,))
    thread_page.start()
    infolist.append(thread_page)

print(infolist)

stop = timeit.default_timer()

print(stop - start)
