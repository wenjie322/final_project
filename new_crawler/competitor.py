# 本程式用於爬各種競爭對手
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
from selenium.webdriver.chrome.options import Options
dict_data = dict()
ffile = input()
ffile = open(ffile, "a", encoding="utf8")
list_dist = ['西區', "中區", "東區", '南區', '北區', '西屯區', '南屯區', '北屯區', '豐原區',
             '大里區', '太平區', '清水區', '沙鹿區',
             '大甲區', '東勢區', '梧棲區', "烏日區",
             "神岡區", "大肚區", "大雅區", "后里區", '霧峰區', '潭子區', '龍井區', '外埔區',
             '和平區', '石岡區', '大安區', '新社區']


def Xclicker(button):
    driver.implicitly_wait(50)
    close = driver.find_element_by_xpath(button)
    close.click()


def idclicker(button):
    driver.implicitly_wait(50)
    close = driver.find_element_by_css_selector(button)
    close.click()


# 爬蟲開始
for dist in list_dist:
    ffile.writelines("________________換區線________________"+"\n")
    list_single_data = []
    chrome_driver_path = r"C:\Users\mikes\Desktop\python\crawler.practice\chromedriver\chromedriver.exe"

    driver = webdriver.Chrome(chrome_driver_path)

    url = "https://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do"
    url = driver.get(url)
    keyword = driver.find_element_by_css_selector("#qryCond")
    driver.implicitly_wait(50)
    keyword.send_keys("台中市"+dist)  # 輸入地區
    # 勾選各種項目
    idclicker("#infoAddr")
    Xclicker(
        '//*[@id="queryListForm"]/div[1]/div[1]/div/div[4]/div[2]/div/div/div/input[5]')
    Xclicker(
        '//*[@id="queryListForm"]/div[1]/div[1]/div/div[4]/div[2]/div/div/div/input[1]')
    idclicker("#isAliveY")
    Xclicker('//*[@id="advSearchIsOff"]/a')
    Xclicker('//*[@id="roundedBox"]/div[1]/div/label[8]')
    Xclicker('//*[@id="busiItemMain"]')
    Xclicker('//*[@id="busiItemMain"]/option[7]')
    Xclicker('//*[@id="busiItemSub"]')
    Xclicker('//*[@id="busiItemSub"]/option[192]')
    time.sleep(1)
    idclicker("#qryBtn")  # 查詢開始

    # 確認這區的資料有幾頁
    driver.implicitly_wait(10)
    page = driver.find_element_by_xpath(
        '//*[@id="queryListForm"]/div[3]/div/div/div/div/div[1]/div[1]')
    page = page.text.strip()
    list_page = page.split("、")
    page = list_page[1]
    page = page.strip("分")
    page = page.strip("頁")
    page = int(page)
    print(dist, page)
    number = int(2)
    for page_c in range(1, page+1):
        if page_c != 1:
            if page_c % 10 == 2 and page_c != 2:
                if page_c == 12:
                    number = number-8
                    driver.find_element_by_xpath(
                        '//*[@id="QueryList_queryList"]/div/div/div/div/nav/ul/li[' + str(number) + ']/a').click()
                else:
                    number = number-9
                    driver.find_element_by_xpath(
                        '//*[@id="QueryList_queryList"]/div/div/div/div/nav/ul/li[' + str(number) + ']/a').click()
            else:
                number += 1
                driver.find_element_by_xpath(
                    '//*[@id="QueryList_queryList"]/div/div/div/div/nav/ul/li[' + str(number) + ']/a').click()

        # 一頁20筆資料，逐筆抓資料
        for i in range(1, 21):
            driver.find_element_by_xpath('//*[@id="viewTable"]/a').click()

            time.sleep(0.5)
            try:
                driver.find_element_by_xpath(
                    '//*[@id="eslist-table"]/tbody/tr[' + str(i) + ']/td[4]/a').click()

            except:
                break
            # 抓名稱
            name = driver.find_element_by_xpath(
                '//*[@id="tabBusmContent"]/div/table/tbody/tr[5]/td[2]')
            name = name.text.split(" ")
            name = name[0]
            # 地址抓取

            addr = driver.find_element_by_xpath(
                '//*[@id="tabBusmContent"]/div/table/tbody/tr[8]/td[2]')
            if "臺中市" not in addr.text:
                addr = driver.find_element_by_xpath(
                    '//*[@id="tabBusmContent"]/div/table/tbody/tr[9]/td[2]')
            if "臺中市" not in addr.text:
                addr = driver.find_element_by_xpath(
                    '//*[@id="tabBusmContent"]/div/table/tbody/tr[10]/td[2]')
            if "臺中市" not in addr.text:
                addr = driver.find_element_by_xpath(
                    '//*[@id="tabBusmContent"]/div/table/tbody/tr[11]/td[2]')
            addr = addr.text.strip("  電子地圖")
            # 抓類別
            driver.find_element_by_xpath('//*[@id="tabOthers"]').click()
            item = driver.find_element_by_xpath(
                '//*[@id="tabOthersContent"]/div[1]/table/tbody/tr[1]/td[1]')
            item = item.text.strip()

            list_single_data.append([name, addr, item])
            print(name, page_c, addr)
            ffile.writelines(name+"   ")
            ffile.writelines(addr+"   ")
            ffile.writelines(item+"\n")
            driver.find_element_by_xpath(
                '//*[@id="bs-example-navbar-collapse-1"]/ul/li[3]/a').click()

            time.sleep(2)
    dict_data[dist] = list_single_data
    driver.close()
    time.sleep(2)
print(dict_data)
