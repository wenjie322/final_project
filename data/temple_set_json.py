import json

with open('temple.txt', 'r', encoding = 'utf-8') as f:
	temp_list = f.readlines()

new_temp_list = []
for temp in temp_list:
	if temp != "───────────────換區線───────────────\n":
		temp_datas = temp.strip().split("   ")
		new_temp_list.append(temp_datas)
print(new_temp_list)


temp_dict = dict()
for temp_data in new_temp_list:
	addr = temp_data[0]
	dist = addr[addr.find("市")+1:addr.find("區")+1]
	print(dist)
	if dist in temp_dict.keys():
		temp_dict[dist].append(temp_data)
	else:
		temp_dict[dist] = [temp_data]

with open('temple.json', 'w+', encoding = 'utf-8') as f:
	f.write(json.dumps(temp_dict, ensure_ascii = False, indent = 2))