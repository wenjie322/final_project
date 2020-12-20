import urllib.request
from bs4 import BeautifulSoup
import json

url = 'https://sheethub.com/ronnyvvang/%E4%BA%BA%E5%8F%A3%E5%AF%86%E5%BA%A6%E8%B3%87%E6%96%99/sql?sql=SELECT%20*%20FROM%20%22ronnyvvang%2F%E4%BA%BA%E5%8F%A3%E5%AF%86%E5%BA%A6%E8%B3%87%E6%96%99%22&page=63&fbclid=IwAR0uC1uR3_ZrnnTtJUShm5Vyn8m7kmQAGN2pjw8kzEI3KGPSlLsqO1-9Zu0.html'
response = urllib.request.urlopen(url)
html = response.read()
sp = BeautifulSoup(html.decode('utf-8'),features="lxml") 

tby = sp.find('tbody')
trs = tby.find_all('tr')

area_dict = dict()
area_dict["里名"] = "面積"
for i in range(0, len(trs)):
	tds = trs[i].find_all('td')
	dis = tds[2].get_text().strip()
	key = tds[3].get_text().strip()
	if dis == "梧棲區":
		area_dict[key] = float(tds[7].get_text().strip())

with open('面積.json', 'w+', encoding = 'utf-8') as f:
	f.write(json.dumps(area_dict, ensure_ascii = False, indent = 2))