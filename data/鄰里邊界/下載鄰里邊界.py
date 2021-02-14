# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:17:19 2021

@author: Brian Ho
"""
import requests
from bs4 import BeautifulSoup
import os, sys

def DownLoad():
    for i in range(3):
        url_num = str(46236253 + i) # Final：46236735
        url = "https://sheethub.com/data.gov.tw/%E6%9D%91%E9%87%8C%E7%95%8C%E5%9C%96%28WGS84%E7%B6%93%E7%B7%AF%E5%BA%A6%29/uri/" + url_num
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        se = soup.find_all('td')
        鄰里名稱 = se[13].get_text()
        區 = se[37].get_text()
        if "?" in 鄰里名稱:
            print("Error：" + url_num, 鄰里名稱, 區, sep=', ')
            continue
        if i == 99:
            print("Final：" + url_num)
        #print(os.path.realpath(sys.argv[0]).strip(sys.argv[0])+ "\\" + 區 + "\\" + 鄰里名稱 + ".json")
        #with open(os.path.dirname(sys.argv[0]) + "\\" + 區 + "\\" + 鄰里名稱 + ".json", 'a+', encoding = 'utf-8') as fh:
        target_json_url = "https://sheethub.com/data.gov.tw/%E6%9D%91%E9%87%8C%E7%95%8C%E5%9C%96%28WGS84%E7%B6%93%E7%B7%AF%E5%BA%A6%29/uri/" + url_num + "?format=geojson"
        #fh.write(requests.get(target_json_url).text)
        jj = requests.get(target_json_url).text
        print(jj)
DownLoad()
    