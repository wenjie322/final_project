# 本程式用於爬於第一次搜尋時，不慎抓錯的餐館
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
from selenium.webdriver.chrome.options import Options
list_shop = []
dict_data = dict()
ffile = input()
ffile = open(ffile, "r", encoding="utf8")
sfile = input()
sfile = open(sfile, "a", encoding="utf8")
for line in ffile:
    shop = line.strip("\n")
    shop = line.strip(" ")
    list_shop.append(shop)


def Xclicker(button):
    driver.implicitly_wait(10)
    close = driver.find_element_by_xpath(button)
    close.click()


def idclicker(button):
    driver.implicitly_wait(10)
    close = driver.find_element_by_css_selector(button)
    close.click()


# 爬蟲開始
for shop in list_shop:
    time.sleep(2)
    chrome_driver_path = r"C:\Users\mikes\Desktop\python\crawler.practice\chromedriver\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    driver = webdriver.Chrome(chrome_driver_path, options=options)

    url = "https://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do"
    url = driver.get(url)

    # 勾選各種項目
    Xclicker(
        '/html/body/div[2]/form/div[1]/div[1]/div/div[4]/div[1]/div/div/div/input[1]')
    # 依店家名稱

    Xclicker(
        '/html/body/div[2]/form/div[1]/div[1]/div/div[4]/div[2]/div/div/div/input[5]')
    # 勾選商業選項

    Xclicker(
        '/html/body/div[2]/form/div[1]/div[1]/div/div[4]/div[2]/div/div/div/input[1]')
    # 取消公司選項

    idclicker("#isAliveY")
    # 勾選現存店家

    Xclicker('//*[@id="advSearchIsOff"]/a')
    # 進階搜尋
    Xclicker('//*[@id="roundedBox"]/div[1]/div/label[8]')
    Xclicker('//*[@id="busiItemMain"]')
    Xclicker('//*[@id="busiItemMain"]/option[7]')
    Xclicker('//*[@id="busiItemSub"]')
    Xclicker('//*[@id="busiItemSub"]/option[192]')

    keyword = driver.find_element_by_css_selector("#qryCond")
    driver.implicitly_wait(10)
    keyword.send_keys(shop)  # 輸入店名
    # idclicker("#qryBtn")  # 查詢開始
    time.sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div[2]/form/div[3]/div/div/div/div/div[2]/div/div[1]/a').click()

    # driver.find_element_by_xpath(
    # '//*[@id="eslist-table"]/tbody/tr[1]/td[4]/a').click()
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
    dict_data[shop] = addr
    sfile.writelines(shop+" ")
    sfile.writelines(addr+"\n")
    shop = shop.strip("\n")
    print(shop, addr)
    driver.close()
print(dict_data)
