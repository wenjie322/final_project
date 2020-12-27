import 爬蟲_地址轉經緯度 as co
import concurrent.futures

shop_dic = co.get_json_data("競爭對手.json")
shop_keys = []
shop_addrs = []
for key in shop_dic:
	shop_keys.append(key)
	shop_addrs.append(shop_dic[key][0])
print(shop_addrs[0])
print(co.get_coordinate(shop_addrs[0]))

# def scrape(addr):
# 	print(co.get_coordinate(addr))
# 	return(co.get_coordinate(addr))

# coor_dic = dict()
# new_shop_dic = shop_dic.copy()
# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
# 	for key, coo in zip(shop_keys, executor.map(scrape, shop_addrs)):
# 		coor_dic[key] = coo

# for key in coor_dic:
# 	new_shop_dic[key].append(coor_dic[key])

# co.write_json_data("競爭對手(co).json", new_shop_dic)