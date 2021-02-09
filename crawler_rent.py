# 本程式是爬台中市各區的店租資料，輸出形式為字典，輸入區名可以得到該區的店租list
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse

list_dist = ["中區", "東區", '西區', '南區', '北區', '西屯區', '南屯區', '北屯區', '豐原區',
             '大里區', '太平區', '清水區', '沙鹿區', '大甲區', '東勢區', '梧棲區',
             "烏日區", "神岡區", "大肚區", "大雅區", "后里區", '霧峰區', '潭子區', '龍井區', '外埔區', '和平區', '石岡區', '大安區', '新社區']
list_dist_url = []
for i in range(len(list_dist)):
    list_dist_url.append(urllib.parse.quote(
        list_dist[i]) + urllib.parse.quote("店面"))

dict_dist_rent = dict()
for k in range(len(list_dist_url)):
    dist = list_dist_url[k]
    rent_list = []
    url = 'https://tw.mixrent.com/search.php?q=' + \
        dist+'&pmin=&pmax=&smin=&smax=&page='
    print(list_dist[k], url)
    for i in range(1, 100):
        url = url + str(i)

        response = urllib.request.urlopen(url)
        html = response.read()
        if html != "":
            sp = BeautifulSoup(html.decode('utf-8'), "lxml")

            a = sp.find_all(class_='house_title')
            plain_s = sp.find_all(class_='label label-success')
            price_s = sp.find_all(class_='label label-primary')
            address_s = sp.find_all(class_="house_address")
            for i in range(0, len(a)):
                rent_name = a[i].get_text().strip()
                address = address_s[i].get_text().strip()
                h = a[i].get('href')
                plain = plain_s[i].get_text().strip()
                price = price_s[i].get_text().strip("$").strip()
                if "台中市" + str(list_dist[k]) in address:
                    rent_list.append([rent_name, address, h, plain, price])
    dict_dist_rent[list_dist[k]] = rent_list
print(dict_dist_rent)
