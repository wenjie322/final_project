import xlrd
import json
import os

data1 = xlrd.open_workbook("wages.xlsx")
table = data1.sheets()[0]
n_rows = table.nrows
n_cols = table.ncols
data = {}
data[table.row_values(0)[2]] = [table.row_values(0)[d] for d in range(3, n_cols)]
for i in range(1, n_rows):
	values = table.row_values(i)
	if values[1] == "梧棲區":
			data[values[2]] = [values[d] for d in range(3, n_cols)]
print(data)

with open('所得.json', 'w+', encoding = 'utf-8') as f:
	f.write(json.dumps(data, ensure_ascii = False, indent = 2))