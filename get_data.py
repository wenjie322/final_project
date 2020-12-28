import json
import os,sys


def get_all_data(filename):
	with open(os.path.realpath(sys.argv[0]).strip(sys.argv[0])+"data\\"+filename, 'r', encoding = 'utf-8') as f:
		dic = json.load(f)
	return dic

def get_data_by_neighborhood(filename, neighborhood):
	dic_all = get_all_data(filename)
	dic = dict()
	for key in dic_all:
		if key == neighborhood:
			dic[key] = dic_all[key]
	return dic

def get_temp_codata(neighborhood):
	dic_temp = get_all_data('廟co.json')
	dic = dict()
	for key in dic_temp:
		pos = dic_temp[key][0].find('里')
		neigh = dic_temp[key][0][pos-2 : pos+1]
		if neigh not in dic:
			dic[neigh] = [{'name':key, 'addr':dic_temp[key][0], 'coor':dic_temp[key][1]}]
		else:
			dic[neigh].append({'name':key, 'addr':dic_temp[key][0], 'coor':dic_temp[key][1]})
	try:
		return(dic[neighborhood])
		pass
	except KeyError:
		return ["no data"]

def get_rent_codata(neighborhood):
	dic_rent = get_all_data('店租co.json')
	dic = dict()
	for key in dic_rent:
		pos = dic_rent[key][1].find('里')
		neigh = dic_rent[key][1][pos-2 : pos+1]
		if neigh not in dic:
			dic[neigh] = [{'name':dic_rent[key][0], 'addr':dic_rent[key][1], 'coor':dic_rent[key][-1], 
			'web':dic_rent[key][2], 'size':dic_rent[key][3], 'price':dic_rent[key][4]}]
		else:
			dic[neigh].append({'name':dic_rent[key][0], 'addr':dic_rent[key][1], 'coor':dic_rent[key][-1],
			 'web':dic_rent[key][2], 'size':dic_rent[key][3], 'price':dic_rent[key][4]})
	try:
		return(dic[neighborhood])
		pass
	except KeyError:
		return ["no data"]

def get_shop_codata(neighborhood, class_list):
	dic_shop = get_all_data('競爭對手co.json')
	dic = dict()
	for key in dic_shop:
		pos = dic_shop[key][0].find('里')
		neigh = dic_shop[key][0][pos-2 : pos+1]
		c_list = []
		for c in dic_shop[key][1]:
			pos = c.find('(')
			n_c = c.strip(c[pos:])
			c_list.append(n_c)
		if neigh not in dic:
			dic[neigh] = [{'name':key, 'addr':dic_shop[key][0], 'coor':dic_shop[key][-1], 'class':c_list}]
		else:
			dic[neigh].append({'name':key, 'addr':dic_shop[key][0], 'coor':dic_shop[key][-1], 'class':c_list})
	selected_list = []
	try:
		for shop in dic[neighborhood]:
			for cl in class_list:
				if cl in shop['class']:
					shop['class'] = cl
					selected_list.append(shop)
					break
	except KeyError:
		pass
	if selected_list == []:
		return ["no data"]
	else:
		return selected_list


# print(get_shop_codata('中正里', ['餐館、餐廳']))
# if __name__ == '__main__':
# 	print(os.path.realpath(sys.argv[0]).strip(sys.argv[0])+"data\\")
# 	data = get_all_data("面積.json")
# 	print(data)
