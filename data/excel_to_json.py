import xlrd
import json
import os

data1 = xlrd.open_workbook("宗教團體查詢結果.xlsx")
table = data1.sheets()[0]
n_rows = table.nrows
n_cols = table.ncols
data = {}
for i in range(3, n_rows):
	values = table.row_values(i)
	data[values[0]] = [values[3]+values[4]]
print(data)

with open('廟.json', 'w+', encoding = 'utf-8') as f:
	f.write(json.dumps(data, ensure_ascii = False, indent = 2))