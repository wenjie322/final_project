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
    chrome_driver_path = r"C:\Users\mikes\Desktop\python\crawler.practice\chromedriver\chromedriver.exe"
    browser = webdriver.Chrome(chrome_driver_path, options=options)
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
ffile = open(ffile, "r", encoding="utf8")
rent_keys = []
rent_addrs = []

comp_dict = dict()
for line in ffile:
    list_line = line.split("  ")
    if len(list_line) > 1:
        if "臺中市" in list_line[1]:
            key = str(list_line[0])
            addr = str(list_line[1])
            comp_dict[str(list_line[0])] = str(list_line[1])
            rent_addrs.append(addr)
            rent_keys.append(key)

new_rent_dic = comp_dict.copy()
print(rent_keys)


def scrape(addr):
    print(get_coordinate(addr))
    return(get_coordinate(addr))


coor_dic = dict()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for key, coo in zip(rent_keys, executor.map(scrape, rent_addrs)):
        coor_dic[key] = coo
for key in coor_dic:
    new_rent_dic[key].append(coor_dic[key])

print(new_rent_dic)
