import json

with open('compete_final.txt', 'r', encoding = 'utf-8') as f:
	shops_list = f.readlines()

new_shop_list = []
for i in range(len(shops_list)):
	if (i%2) == 0:
		shops_list[i] = shops_list[i].strip().split(" ")
		new_shop_list.append(shops_list[i])
# print(new_shop_list)

shop_dict = dict()
for shop_data in new_shop_list:
	addr = shop_data[1]
	dist = addr[addr.find("市")+1:addr.find("區")+1]
	print(dist)
	if dist in shop_dict.keys():
		shop_dict[dist].append(shop_data)
	else:
		shop_dict[dist] = [shop_data]

with open('compete.json', 'w+', encoding = 'utf-8') as f:
	f.write(json.dumps(shop_dict, ensure_ascii = False, indent = 2))