# 爬取廟宇資料
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
from selenium.webdriver.chrome.options import Options

file_name = "temple"
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

the_driver = r"C:\Users\King\Desktop\爬蟲\chromedriver"
driver = webdriver.Chrome(the_driver)
for times in range(1, 30):
    the_file.writelines("───────────────換區線───────────────"+"\n")
    print("───────────────換區線───────────────")
    url = driver.get("https://religion.moi.gov.tw/Religion/FoundationTemple?ci=1")
    Xclicker('//*[@id="Country"]/option[10]')  
    addr = "//*[@id='Area']/option[" + str(times+1) + "]"
    Xclicker(addr)
    time.sleep(2)
    Xclicker2('//*[@id="RT"]')
    Xclicker2('//*[@id="RLT"]')
    Xclicker2('//*[@id="SubmitForm"]/div[1]/div[3]/input')

    driver.implicitly_wait(10)
    page = driver.find_element_by_xpath('//*[@id="pg02_data"]/div[1]/div[4]').text.strip()
    a = page.find('共')
    b = a + page[a:].find('頁')
    page = int(page[a+1:b])
    print(page)

    for page_c in range(1, page+1):
        for i in range(1, 21):
            try:
                element = '//*[@id="pg02_data"]/div[2]/table/tbody/tr[' + str(i) + ']'
                driver.find_element_by_xpath(element)
                name_element = element + "/td[1]"
                dist_element = element + "/td[4]"
                addr_element = element + "/td[5]"
                name = driver.find_element_by_xpath(name_element).text
                dist = driver.find_element_by_xpath(dist_element).text
                addr = driver.find_element_by_xpath(addr_element).text
                print(dist+addr, name)
                the_file.writelines(dist+addr+"   ")
                the_file.writelines(name+"\n")
            except:
                break
        driver.implicitly_wait(10)
        if page_c != page:
            next_page = '//*[@id="pg02_data"]/div[1]/div[4]/a[' + str(page_c+1) + ']'
            Xclicker2(next_page)
