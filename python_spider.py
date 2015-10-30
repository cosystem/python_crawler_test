# -*- coding: utf-8 -*-
__author__ = 'PGY'
import timeit
start = timeit.default_timer()
from threading import Thread
import requests
import re
from bs4 import BeautifulSoup, SoupStrainer

def get_single_item_data(item_url, header):
    '''function to get the room images and info in each page'''
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"}
    # get the page source and parse the code
    source_code = requests.get(item_url, headers=headers)
    plain_text = source_code.text.encode('utf-8', 'ignore')
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
    return (imglist, roominfodict)

def get_rooms(page):
    '''function to get all the room information with specified page number'''
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"}
    allimginfolist = []
    tag_hosts = set()    # set to save all tags
    url = "http://zu.fang.com/house/"
    url = url + "i3" + str(page)
    source_code = requests.get(url, headers=headers)
    plain_text = source_code.text
    titles = SoupStrainer('p',{'class': 'title'})
    soup = BeautifulSoup(plain_text, "html.parser", parse_only=titles)
    all_a_tag = soup.find_all('a', {'href': re.compile('.+')})
    all_a_tag.pop()

    # save all links in a page to a set data structure
    for tag in all_a_tag:
        href = "http://zu.fang.com" + tag.get('href')
        tag_hosts.add(href)

    # multithread process through the all links saved in the set
    threadlist = []
    for link in tag_hosts:
        thread_host = Thread(target = get_single_item_data, args=(link,))
        thread_host.start()
        threadlist.append(thread_host)

    # ensure all of the threads have finished
    for j in threadlist:
        j.join()

# iterate through all pages and create thread for each page and append each thread to the infolist
threadlist = []
pagenumber = 2
for i in range(1,pagenumber+1):
    thread_page = Thread(target=get_rooms, args=(i,))
    thread_page.start()
    threadlist.append(thread_page)

# ensure all of the threads have finished
for j in threadlist:
    j.join()

stop = timeit.default_timer()

print(stop - start)
