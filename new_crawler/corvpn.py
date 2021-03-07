import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import json
import concurrent.futures
import time

options = webdriver.ChromeOptions()
options.add_extension(
    r'C:\Users\mikes\Desktop\python\crawler.practice\vpn\7.0.6_0.crx')
# options.add_argument("headless")
options.add_argument("disable-infobars")
options.add_experimental_option('excludeSwitches', ['enable-logging'])


def get_coordinate(addr):
    chrome_driver_path = r"C:\Users\mikes\Desktop\python\crawler.practice\chromedriver\chromedriver.exe"
    browser = webdriver.Chrome(chrome_driver_path, options=options)

    # 進入搜尋網站
    browser.get("http://www.map.com.tw/")
    search = browser.find_element_by_id("searchWord")
    search.clear()
    search.send_keys(addr)
    browser.find_element_by_xpath(
        "/html/body/form/div[10]/div[2]/img[2]").click()
    time.sleep(2)
    iframe = browser.find_elements_by_tag_name("iframe")[1]
    browser.switch_to.frame(iframe)
    coor_btn = browser.find_element_by_xpath(
        "/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")

    coor_btn.click()
    coor = browser.find_element_by_xpath(
        "/html/body/form/div[5]/table/tbody/tr[2]/td")

    coor = coor.text.strip().split(" ")
    lat = coor[-1].split("：")[-1]
    log = coor[0].split("：")[-1]
    browser.close()
    return [lat, log]


ffile = input()
file2 = input()
ffile = open(ffile, "r", encoding="utf8")
rent_keys = []
rent_addrs = []

file2 = open(file2, "r", encoding="utf-8")

list_file2 = []
for line in file2:
    element = line.strip(" ")
    element = element.strip("\n")
    list_file2.append(element)

dict_file2 = dict()
for i in range(len(list_file2)):
    if i % 2 == 0:
        key = list_file2[i]
    else:
        dict_file2[key] = list_file2[i]


# 將第一份資料和第二資料整合成字典
comp_dict = dict()
list_shop = []
list_address = []
for line in ffile:
    if line != '________________換區線________________\n':
        list_line = line.split("  ")

        if "臺中市" not in str(list_line[1]):
            list_line[1] = dict_file2[str(list_line[0])]
        shop = list_line[0]
        location = list_line[1]
        list_shop.append(shop)
        list_address.append(location)
        comp_dict[shop] = location


new_rent_dic = comp_dict.copy()


def scrape(addr):
    print(get_coordinate(addr))
    return(get_coordinate(addr))


coor_dic = dict()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for key, coo in zip(list_shop, executor.map(scrape, list_address)):
        coor_dic[key] = coo
for key in coor_dic:
    new_rent_dic[key].append(coor_dic[key])

print(new_rent_dic)
