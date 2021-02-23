# 爬取人口消長資料
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
from selenium.webdriver.chrome.options import Options

file_name = "edu"
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

def comma_deleter(number):
    number_list = []
    last_loc = -1
    for i in range(len(number)):
        if number[i] == ',':
            number_list.append(number[last_loc+1:i])
            last_loc = i
    number_list.append(number[last_loc+1:])
    new_number = ''
    for i in range(len(number_list)):
        new_number += number_list[i]
    new_number = int(new_number)
    return new_number

the_driver = r"C:\Users\user\Desktop\Studies\PBC\Final Project\crawler\chromedriver"
driver = webdriver.Chrome(the_driver)
url = driver.get("https://demographics.taichung.gov.tw/Demographic/WebPage/TCCReport13.html?s=10683756")
time.sleep(2)

for times in range(1, 30):
    out = 0
    the_file.writelines("───────────────換區線───────────────"+"\n")
    print("───────────────換區線───────────────")
    addr = '/html/body/div[2]/div/div/div[2]/div[1]/div[1]/div/div[2]/select/option[' + str(times+1) + ']'
    Xclicker(addr)
    time.sleep(2)
    Xclicker2('/html/body/div[2]/div/div/div[2]/div[1]/div[1]/div/div[5]/button')
    time.sleep(6)

    Xclicker2('//*[@id="statisticsTable"]/thead/tr[1]/th[4]')
    Xclicker2('//*[@id="statisticsTable"]/thead/tr[1]/th[4]')
    page = driver.find_element_by_xpath('//*[@id="statisticsTable_info"]').text.strip()
    a = page.find('共')
    b = a + page[a:].find('頁')
    print(page)
    page = int(page[a+2:b-1])
    print(page)
    disc_element = '//*[@id="statisticsTable"]/tbody/tr[1]/td[2]'
    disc = driver.find_element_by_xpath(disc_element).text
    print(disc)

    for page_c in range(1, page+1):
        if out == 1:
            break
        for i in range(1, 11):
            try:
                tag = '//*[@id="statisticsTable"]/tbody/tr['
                vill_element = tag + str(i) + ']/td[3]'
                key_element = tag + str(i) + ']/td[4]'
                vill = driver.find_element_by_xpath(vill_element).text
                key_word = driver.find_element_by_xpath(key_element).text
                if key_word != '總計':
                    out = 1
                    break
                if vill != '全部':
                    grad_element = tag + str(i) + ']/td[6]'
                    number = driver.find_element_by_xpath(grad_element).text
                    grad_number = comma_deleter(number)
                    grad_element = tag + str(i) + ']/td[8]'
                    number = driver.find_element_by_xpath(grad_element).text
                    grad_number += comma_deleter(number)

                    univ_element = tag + str(i) + ']/td[10]'
                    number = driver.find_element_by_xpath(univ_element).text
                    univ_number = comma_deleter(number)
                    univ_element = tag + str(i) + ']/td[12]'
                    number = driver.find_element_by_xpath(univ_element).text
                    univ_number += comma_deleter(number)
                    univ_element = tag + str(i) + ']/td[14]'
                    number = driver.find_element_by_xpath(univ_element).text
                    univ_number += comma_deleter(number)

                    sh_element = tag + str(i) + ']/td[16]'
                    number = driver.find_element_by_xpath(sh_element).text
                    sh_number = comma_deleter(number)
                    sh_element = tag + str(i) + ']/td[18]'
                    number = driver.find_element_by_xpath(sh_element).text
                    sh_number += comma_deleter(number)

                    jh_element = tag + str(i) + ']/td[21]'
                    number = driver.find_element_by_xpath(jh_element).text
                    jh_number = comma_deleter(number)
                    jh_element = tag + str(i) + ']/td[23]'
                    number = driver.find_element_by_xpath(jh_element).text
                    jh_number += comma_deleter(number)
                    jh_element = tag + str(i) + ']/td[25]'
                    number = driver.find_element_by_xpath(jh_element).text
                    jh_number += comma_deleter(number)

                    data = '台中市' + disc + vill + ' '
                    data+= str(jh_number) + ','
                    data+= str(sh_number) + ','
                    data+= str(univ_number) + ','
                    data+= str(grad_number)
                    print(data)
                    the_file.writelines(data+"\n")
            except:
                break
        if page_c != page:
            if page_c >= 5 and page_c < page-2:
                next_page = '//*[@id="statisticsTable_paginate"]/ul/li[6]'
            elif page_c >= page-2:
                next_page = '//*[@id="statisticsTable_paginate"]/ul/li[' + str(9+page_c-page) + ']'
            else:
                next_page = '//*[@id="statisticsTable_paginate"]/ul/li[' + str(page_c+2) + ']'
            Xclicker2(next_page)