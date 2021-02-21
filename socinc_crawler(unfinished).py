# 爬取人口消長資料
# 未完成
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
from selenium.webdriver.chrome.options import Options

file_name = "socinc"
the_file = open(file_name, "w", encoding="utf8")
# 台中總共29個區

def Xclicker(button):
    driver.implicitly_wait(50)
    close = driver.find_element_by_xpath(button)
    close.click()

def idclicker(button):
    driver.implicitly_wait(50)
    close = driver.find_element_by_id(button)
    close.click()

def classclicker(button):
    driver.implicitly_wait(50)
    close = driver.find_element_by_class_name(button)
    close.click()
    
def Xclicker2(button): # 使用時機：若使用Xclicker出現not clickable的bug時
    driver.implicitly_wait(50)
    close = driver.find_element_by_xpath(button)
    driver.execute_script("arguments[0].click();", close)

the_driver = r"C:\Users\user\Desktop\Studies\PBC\Final Project\drive-download-20210211T083703Z-001\chromedriver"
driver = webdriver.Chrome(the_driver)
url = driver.get("https://demographics.taichung.gov.tw/Demographic/WebPage/TCCReport04.html?s=10683756")
time.sleep(2)
Xclicker('/html/body/div[2]/div/div/div[2]/div[1]/div[1]/div/div[1]/select/option[2]')
Xclicker('/html/body/div[2]/div/div/div[2]/div[1]/div[1]/div/div[2]/select/option[1]')
for times in range(1, 2):
    the_file.writelines("───────────────換區線───────────────"+"\n")
    print("───────────────換區線───────────────")
    addr = '/html/body/div[2]/div/div/div[2]/div[1]/div[1]/div/div[3]/select/option[' + str(times+1) + ']'
    Xclicker(addr)
    time.sleep(2)
    Xclicker2('/html/body/div[2]/div/div/div[2]/div[1]/div[1]/div/div[6]/button')
    time.sleep(2)

    page = driver.find_element_by_xpath('//*[@id="statisticsTable_info"]').text.strip()
    a = page.find('共')
    b = a + page[a:].find('頁')
    page = int(page[a+2:b-1])
    print(page)