import get_data as gd

'''取json檔所有資料
get_all_data("面積.json") 取面積資料
get_all_data("人口結構.json") 取人口結構資料
get_all_data("所得.json") 取所得資料
get_all_data("性別.json") 取性別資料
get_all_data("社會增加.json") 取社會增加資料
get_all_data("教育程度.json") 取教育程度資料
'''
d = gd.get_all_data("面積.json")

#取單一里資料
d_a = gd.get_data_by_neighborhood("性別.json","頂寮里")

print(d)
print(d_a)