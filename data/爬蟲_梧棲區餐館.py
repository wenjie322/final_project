import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import concurrent.futures
import json

# shop_dic = dict()
# options = webdriver.ChromeOptions()
# # options.add_argument("headless")
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# browser = webdriver.Chrome(options=options)
# browser.get("https://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do")
# browser.find_element_by_id('infoAddr').click()
# browser.find_element_by_xpath('//*[@id="queryListForm"]/div[1]/div[1]/div/div[4]/div[2]/div/div/div/input[5]').click()
# browser.find_element_by_xpath('//*[@id="queryListForm"]/div[1]/div[1]/div/div[4]/div[2]/div/div/div/input[1]').click()
# browser.find_element_by_id('isAliveY').click()
# browser.find_element_by_xpath('//*[@id="advSearchIsOff"]/a').click()
# browser.find_element_by_xpath('//*[@id="roundedBox"]/div[1]/div/label[8]/input').click()
# select_1 = Select(browser.find_element_by_id('busiItemMain'))
# select_1.select_by_value('F')
# time.sleep(5)
# select_2 = Select(browser.find_element_by_id('busiItemSub'))
# select_2.select_by_value('F501060')
# ad = browser.find_element_by_id("qryCond")
# ad.send_keys('臺中市梧棲區')
# time.sleep(2)
# browser.find_element_by_id('qryBtn').click()
shop_dic = dict()
def get_data(page):
	global shop_dic
	options = webdriver.ChromeOptions()//*[@id="tabBusmContent"]
	# options.add_argument("headless")
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	browser = webdriver.Chrome(options=options)
	browser.get("https://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do")
	browser.find_element_by_id('infoAddr').click()
	browser.find_element_by_xpath('//*[@id="queryListForm"]/div[1]/div[1]/div/div[4]/div[2]/div/div/div/input[5]').click()
	browser.find_element_by_xpath('//*[@id="queryListForm"]/div[1]/div[1]/div/div[4]/div[2]/div/div/div/input[1]').click()
	browser.find_element_by_id('isAliveY').click()
	browser.find_element_by_xpath('//*[@id="advSearchIsOff"]/a').click()
	browser.find_element_by_xpath('//*[@id="roundedBox"]/div[1]/div/label[8]/input').click()
	select_1 = Select(browser.find_element_by_id('busiItemMain'))
	select_1.select_by_value('F')
	time.sleep(5)
	select_2 = Select(browser.find_element_by_id('busiItemSub'))
	select_2.select_by_value('F501060')
	ad = browser.find_element_by_id("qryCond")
	ad.send_keys('臺中市梧棲區')
	time.sleep(2)
	browser.find_element_by_id('qryBtn').click()
	if page != 1:
		browser.find_element_by_xpath('//*[@id="QueryList_queryList"]/div/div/div/div/nav/ul/li[' + str(page+1) +']/a').click()
	for i in range(1,21):
		browser.find_element_by_xpath('//*[@id="viewTable"]/a').click()
		time.sleep(2)
		browser.find_element_by_xpath('//*[@id="eslist-table"]/tbody/tr[' + str(i) +']/td[4]/a').click()
		name = browser.find_element_by_xpath('//*[@id="tabBusmContent"]/div/table/tbody/tr[5]/td[2]')
		name = name.text.strip("  Google搜尋  「國貿局廠商英文名稱查詢(限經營出進口或買賣業務者)」")
		addr = browser.find_element_by_xpath('//*[@id="tabBusmContent"]/div/table/tbody/tr[10]/td[2]')
		addr = addr.text.strip("  電子地圖")
		browser.find_element_by_xpath('//*[@id="tabOthers"]').click()
		item = browser.find_element_by_xpath('//*[@id="tabOthersContent"]/div[1]/table/tbody/tr[1]/td[1]')
		item = item.text.strip()
		shop_dic[name] = [addr,item]
		print(name)
		browser.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[3]/a').click()
		time.sleep(2)

p = [i for i in range(1,6)]
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
	executor.map(get_data, p)

for key in shop_dic:
	shop_dic[key][1] = shop_dic[key][1].split('\n')

print(shop_dic)

with open('競爭對手.json', 'w+', encoding = 'utf-8') as f:
		f.write(json.dumps(shop_dic, ensure_ascii = False, indent = 2))
# for p in range(1,6):
# 	for i in range(1,21):
# 		browser.find_element_by_xpath('//*[@id="viewTable"]/a').click()
# 		time.sleep(2)
# 		browser.find_element_by_xpath('//*[@id="eslist-table"]/tbody/tr[' + str(i) +']/td[4]/a').click()
# 		name = browser.find_element_by_xpath('//*[@id="tabBusmContent"]/div/table/tbody/tr[5]/td[2]')
# 		name = name.text.strip("  Google搜尋  「國貿局廠商英文名稱查詢(限經營出進口或買賣業務者)」")
# 		addr = browser.find_element_by_xpath('//*[@id="tabBusmContent"]/div/table/tbody/tr[10]/td[2]')
# 		addr = addr.text.strip("  電子地圖")
# 		browser.find_element_by_xpath('//*[@id="tabOthers"]').click()
# 		item = browser.find_element_by_xpath('//*[@id="tabOthersContent"]/div[1]/table/tbody/tr[1]/td[1]')
# 		item = item.text.strip()
# 		shop_dic[name] = [addr,item]
# 		print(name)
# 		browser.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[3]/a').click()
# 		time.sleep(2)
# 	if p != 5:
# 		browser.find_element_by_xpath('//*[@id="QueryList_queryList"]/div/div/div/div/nav/ul/li[' + str(p+2) +']/a').click()
# print(shop_dic)
