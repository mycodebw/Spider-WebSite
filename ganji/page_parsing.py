#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import random
import pymongo
import requests
from bs4 import BeautifulSoup

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
url_list = ganji['url_list']
item_info = ganji['item_info']


"""
headers  = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection':'keep-alive'
}


proxy_list = [
    ]
"""

def get_links_from(channel, page, who_sell='o'):
    # http://bj.ganji.com/ershoubijibendiannao/o3/
    url = '{}{}{}/'.format(channel, who_sell, page)
    wb_data = requests.get(url, headers=headers, proxies=proxies)
    if wb_data.status_code == 200:
        soup = BeautifulSoup(wb_data.text, 'lxml')
        for link in soup.select('.fenlei dt a'):
            item_link = link.get('href')
            url_list.insert_one({'url': item_link})
            get_item_info_from(item_link)
   #         print(item_link)

def get_item_info_from(url, data=None):
    wb_data = requests.get(url, headers=headers)
    if wb_data.status_code != 200:
        return
    
    soup = BeautifulSoup(wb_data.text, 'lxml')
    
    prices = soup.select('.f22.fc-orange.f-type')
    pub_dates = soup.select('.pr-5')
    areas = soup.select('ul.det-infor > li:nth-of-type(3) > a')
    cates = soup.select('ul.det-infor > li:nth-of-type(1) > span')
    
    data = {
        'title': soup.title.text.strip(),
        'price': prices[0].text.strip() if len(prices) > 0 else 0,
        'pub_date': pub_dates[0].text.strip().split(' ')[0] if len(pub_dates) > 0 else "",
        'area': [area.text.strip() for area in areas if area.text.strip() != "-"],
        'cates': [cate.text.strip() for cate in cates],
        'url':url
    }
    print(data)
    item_info.insert_one(data)
