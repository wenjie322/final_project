import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import json
import concurrent.futures
import time
import math

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

def get_coordinate(addr):
	browser = webdriver.Chrome(options=options)
	browser.get("https://map.tgos.tw/TGOSCloud/Web/Map/TGOSViewer_Map.aspx?addr="+addr)
	time.sleep(5)
	soup = BeautifulSoup(browser.page_source, 'html.parser')
	p = soup.find('p', attrs={'style':'white-space: nowrap'})
	tx = float(p.get_text().split('：')[-2].strip('Y坐標'))
	ty = float(p.get_text().split('：')[-1].strip())
	y = ty * 0.00000899823754
	x = 121 + (tx - 250000) * 0.000008983152841195214 / math.cos(math.radians(y))
	browser.close()
	return [y,x]
	# ty = browser.find_element_by_xpath('//*[@id="MapBox"]/div[1]/div[2]/div/p[1]/text()')
	# print(ty)

def get_json_data(j_path):
	with open(j_path, 'r', encoding = 'utf-8') as f:
		dic = json.load(f)
	return dic

def write_json_data(j_path, data):
	with open(j_path, 'w+', encoding = 'utf-8') as f:
		f.write(json.dumps(data, ensure_ascii = False, indent = 2))

shop_dic = get_json_data("競爭對手.json")
shop_keys = []
shop_addrs = []
coor_dic = dict()
new_shop_dic = shop_dic.copy()
for key in shop_dic:
	shop_keys.append(key)
	shop_addrs.append(shop_dic[key][0])

def scrape(addr):
	print(get_coordinate(addr))
	return(get_coordinate(addr))

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
	for key, coo in zip(shop_keys, executor.map(scrape, shop_addrs)):
		coor_dic[key] = coo
		print(key)

for key in coor_dic:
	new_shop_dic[key].append(coor_dic[key])

print(new_shop_dic)

write_json_data('競爭對手co.json', new_shop_dic)

# python 店家地址轉經緯度.py