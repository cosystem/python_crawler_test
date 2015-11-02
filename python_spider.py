# -*- coding: utf-8 -*-
__author__ = 'PGY'
import timeit
start = timeit.default_timer()
import threading
import requests
import re
import socket
import time
import random, math
from bs4 import BeautifulSoup, SoupStrainer


#socket.setdefaulttimeout(30)

def get_single_item_data(item_url):
    '''function to get the room images and info in each page'''
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"}
    # get the page source and parse the code
    source_code = requests.get(item_url, headers=headers, timeout=5)
    plain_text = source_code.text.encode('utf-8', 'ignore')
    images_and_info = SoupStrainer(['div', {'class': 'img01'}, 'script', {'type': 'text/javascript'}])
    soup = BeautifulSoup(plain_text, "html.parser", parse_only=images_and_info)
    # get all the links for the images
    all_imgs = soup.find_all('img', {'src': re.compile('.+'), 'name': 'ImgList'})
    # get the image list
    imglist = [img.get('src') for img in all_imgs]
    # get the room information
    allinfo = soup.find('script').get_text()
    roominfo = allinfo.split('var')[1]
    # process the data to save the roominfo properly in dictionary data structure
    roominfolist = roominfo.replace(' ','').replace(',','').replace('\'','').split('\r\n')[1:-3]
    roominfolistnew = [infoitem.split(":") for infoitem in roominfolist]
    #print(roominfolistnew)
    roominfodict = dict(roominfolistnew)
    return (imglist, roominfodict)

def get_rooms(page):
    '''function to get all the room information with specified page number'''
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"}
    allimginfolist = []
    tag_hosts = set()    # set to save all tags
    url = "http://zu.fang.com/house/"
    url = url + "i3" + str(page)
    source_code = requests.get(url, headers=headers, timeout=5)
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
        thread_host = threading.Thread(target = get_single_item_data, args=(link,))
        thread_host.start()
        threadlist.append(thread_host)

    # ensure all of the threads have finished
    for j in threadlist:
        j.join()

def main():
    maxpage = 1
    for page in range(1, maxpage+1):
        get_rooms(page)
        # to control the request speed
        random_interval=random.randrange(1, 5, 1)
        time.sleep(random_interval)

if __name__=="__main__":
    main()

# ensure all of the threads have finished
# for j in threadlist:
#    j.join()

stop = timeit.default_timer()

print(stop - start)
