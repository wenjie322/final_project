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

if __name__ == '__main__':
	print(os.path.realpath(sys.argv[0]).strip(sys.argv[0])+"data\\")
	data = get_all_data("面積.json")
	print(data)