import 爬蟲_地址轉經緯度 as co
import concurrent.futures

temp_dic = co.get_json_data("廟.json")
temp_keys = []
temp_addrs = []
for key in temp_dic:
	temp_keys.append(key)
	temp_addrs.append(temp_dic[key][0])

def scrape(addr):
	print(co.get_coordinate(addr))
	return(co.get_coordinate(addr))

coor_dic = dict()
new_temp_dic = temp_dic.copy()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
	for key, coo in zip(temp_keys, executor.map(scrape, temp_addrs)):
		coor_dic[key] = coo

for key in coor_dic:
	new_temp_dic[key].append(coor_dic[key])

co.write_json_data("廟.json", new_temp_dic)