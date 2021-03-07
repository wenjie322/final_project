# 本程式是爬台中市各區的店租資料，輸出形式為字典，輸入區名可以得到該區的店租list
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse
import selenium
import time
from selenium import webdriver

the_file = open("rent_area", "a", encoding="utf8")

list_dist = ['西區', "中區", "東區", '南區', '北區', '西屯區', '南屯區', '北屯區', '豐原區',
             '大里區', '太平區', '清水區', '沙鹿區',
             '大甲區', '東勢區', '梧棲區', "烏日區",
             "神岡區", "大肚區", "大雅區", "后里區", '霧峰區', '潭子區', '龍井區', '外埔區',
             '和平區', '石岡區', '大安區', '新社區']
# 建立搜尋關鍵字的清單
list_dist_url = []
for i in range(len(list_dist)):
    list_dist_url.append(urllib.parse.quote(
        list_dist[i]) + urllib.parse.quote("店面"))


def Xclicker(button):
    driver.implicitly_wait(10)
    close = driver.find_element_by_xpath(button)
    close.click()


def idclicker(button):
    driver.implicitly_wait(10)
    close = driver.find_element_by_css_selector(button)
    close.click()


# 照關鍵字搜尋
dict_dist_rent = dict()
for k in range(len(list_dist_url)):

    time.sleep(2)
    chrome_driver_path = r"C:\Users\mikes\Desktop\python\crawler.practice\chromedriver\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_path)
    dist = list_dist_url[k]  # 關鍵字原始碼
    dist_real = list_dist[k]
    rent_list = []  # 本區的所有資料
    the_file.writelines(dist_real + ":\n")
    url = 'https://tw.mixrent.com/search.php?q='+dist+"&smin=&smax=&pmin=&pmax="
    url = driver.get(url)

    infro = driver.find_element_by_xpath(
        '/html/body/div[2]/div/div[2]/div[2]/div/div[1]/div/div').text.strip()
    a = infro.find("/")
    b = infro.find("頁")
    # 找到有幾頁
    page = int(infro[a+1:b])
    print(page)

    # 抓資料
    # 第一頁
    for i in range(4, 14):
        try:
            name = driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[2]/div['+str(i)+']/div[1]/div/a').text
            area = driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[2]/div['+str(i)+']/div[2]/div[1]/ul/li[1]/span').text
            location = driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[2]/div['+str(i)+']/div[2]/div[2]/div[1]').text
            if "台中" in location or "臺中" in location:
                if dist_real in location:
                    the_file.writelines(name+" "+area+"\n")
        except:
            driver.close()
            break

    # 除第一頁的
    for k in range(2, page+1):
        print(k)
        if page <= 10:
            Xclicker(
                '/html/body/div[2]/div/div[2]/div[15]/ul/li['+str(k+1)+']/a')
        else:
            if k < 6:
                Xclicker(
                    '/html/body/div[2]/div/div[2]/div[15]/ul/li['+str(k+1)+']/a')
            elif k >= page-3:
                Xclicker(
                    '/html/body/div[2]/div/div[2]/div[15]/ul/li['+str(11-(page-k))+']/a')
            else:
                Xclicker('/html/body/div[2]/div/div[2]/div[15]/ul/li[7]/a')
        for i in range(4, 14):
            try:
                name = driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div[2]/div['+str(i)+']/div[1]/div/a').text
                area = driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div[2]/div['+str(i)+']/div[2]/div[1]/ul/li[1]/span').text
                location = driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div[2]/div['+str(i)+']/div[2]/div[2]/div[1]').text
                if "台中" in location or "臺中" in location:
                    if dist_real in location:
                        the_file.writelines(name+" "+area+"\n")

            except:
                driver.close()
                break
