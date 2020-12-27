import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import json
import concurrent.futures
import time

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

def get_coordinate(addr):
	browser = webdriver.Chrome(options=options)
	browser.get("http://www.map.com.tw/")
	search = browser.find_element_by_id("searchWord")
	search.clear()
	search.send_keys(addr)
	browser.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click() 
	time.sleep(2)
	iframe = browser.find_elements_by_tag_name("iframe")[1]
	browser.switch_to.frame(iframe)
	coor_btn = browser.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
	coor_btn.click()
	coor = browser.find_element_by_xpath("/html/body/form/div[5]/table/tbody/tr[2]/td")
	coor = coor.text.strip().split(" ")
	lat = coor[-1].split("：")[-1]
	log = coor[0].split("：")[-1]
	browser.close()
	return [lat, log]

def get_json_data(j_path):
	with open(j_path, 'r', encoding = 'utf-8') as f:
		dic = json.load(f)
	return dic

def write_json_data(j_path, data):
	with open(j_path, 'w+', encoding = 'utf-8') as f:
		f.write(json.dumps(data, ensure_ascii = False, indent = 2))

'''
rent_dic = get_json_data("店租.json")
rent_keys = []
rent_addrs = []
coor_dic = dict()
new_rent_dic = rent_dic.copy()
for key in rent_dic:
	rent_keys.append(key)
	rent_addrs.append(rent_dic[key][1])

def scrape(addr):
	print(get_coordinate(addr))
	return(get_coordinate(addr))

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
	for key, coo in zip(rent_keys, executor.map(scrape, rent_addrs)):
		coor_dic[key] = coo

for key in coor_dic:
	new_rent_dic[key].append(coor_dic[key])

with open('店租.json', 'w+', encoding = 'utf-8') as f:
	f.write(json.dumps(new_rent_dic, ensure_ascii = False, indent = 2))
'''

# shop_dic = get_json_data("競爭對手co.json")
# shop_keys = []
# shop_addrs = []
# coor_dic = dict()
# new_shop_dic = dict()
# for key in shop_dic:
# 	new_shop_dic[key] = [shop_dic[key][0], shop_dic[key][1]]
# 	shop_keys.append(key)
# 	shop_addrs.append(shop_dic[key][0])
# print(shop_addrs)

# def scrape(addr):
# 	print(get_coordinate(addr))
# 	return(get_coordinate(addr))

# with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
# 	for key, coo in zip(shop_keys, executor.map(scrape, shop_addrs)):
# 		coor_dic[key] = coo

# for key in coor_dic:
# 	new_shop_dic[key].append(coor_dic[key])
# print(new_shop_dic)

# write_json_data("競爭對手co1.json", new_shop_dic)

# with open('店租.json', 'w+', encoding = 'utf-8') as f:
# 	f.write(json.dumps(new_rent_dic, ensure_ascii = False, indent = 2))