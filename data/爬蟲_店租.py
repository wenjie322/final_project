import urllib.request
from bs4 import BeautifulSoup
import json

rent_list = []
for i in range(1,4):
	url = 'https://tw.mixrent.com/search.php?q=%E6%A2%A7%E6%A3%B2%E5%BA%97%E9%9D%A2&pmin=&pmax=&smin=&smax=&page=' + str(i)
	response = urllib.request.urlopen(url)
	html = response.read()
	sp = BeautifulSoup(html.decode('utf-8'),features="lxml")

	a = sp.find_all(class_='house_title')
	plain_s = sp.find_all(class_='label label-success')
	price_s = sp.find_all(class_='label label-primary')
	address_s = sp.find_all(class_="house_address")
	for i in range(0,len(a)):
		rent_name = a[i].get_text().strip()
		address = address_s[i].get_text().strip()
		h = a[i].get('href')
		plain = plain_s[i].get_text().strip()
		price = price_s[i].get_text().strip("$").strip()
		rent_list.append([rent_name, address, h, plain, price])
rent_dic = dict()
i = 1
for rent in rent_list:
	rent_dic["店面" + str(i)] = [rent[d] for d in range(0, len(rent))]
	i += 1

with open('店租.json', 'w+', encoding = 'utf-8') as f:
	f.write(json.dumps(rent_dic, ensure_ascii = False, indent = 2))