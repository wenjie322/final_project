import get_data as gd
d_square = gd.get_all_data("面積.json")
list_dist = ["下寮里", "大村里", "大庄里", "中正里", "中和里", "文化里",
             "永安里", "永寧里", "安仁里", "南簡里", "草湳里", "頂寮里", "福德里", "興農里"]
list_square = []
for dist in list_dist:
    list_square.append(dist, d_square[dist][1])

people_com = input()
result = input()
people_com = open(people_com, "r", encoding="utf8")
result = open(result, "a", encoding="utf8")
Funder18 = dict()
F19to35 = dict()
F36to45 = dict()
Fotherage = dict()
Munder18 = dict()
M19to35 = dict()
M36to45 = dict()
Motherage = dict()
list_1part = []
list_allpart = []
for line in people_com:
    line = line.strip(" ")
    line = line.replace('"', "")
    line = line.strip("\n")
    line = line.strip(",")
    if line != "{" and line != "[" and line != "]" and line != "}":
        if "總計" not in line:
            cut = line.find(":")
            line = line[cut+2:len(line)]
            list_1part.append(line)
        else:
            cut = line.find(":")
            line = line[cut+2:len(line)]
            list_1part.append(line)
            list_allpart.append(list_1part)
            list_1part = []
# print(list_allpart[1])
list_name = []
for dist in list_allpart:
    if dist[2] == '男' and dist[1] == "梧棲區":
        name = dist[0]+dist[1]
        if name not in list_name:
            list_name.append(name)
        Munder18[name] = 0
        M19to35[name] = 0
        M36to45[name] = 0
        Motherage[name] = 0
        for i in range(3, 24):
            if i <= 6:
                number = int(dist[i])
                Munder18[name] += number
            if i > 6 and i <= 9:
                number = int(dist[i])
                M19to35[name] += number
            if i > 9 and i <= 11:
                number = int(dist[i])
                M36to45[name] += number
            else:
                number = int(dist[i])
                Motherage[name] += number

    if dist[2] == '女':
        name = dist[0]+dist[1]
        Funder18[name] = 0
        F19to35[name] = 0
        F36to45[name] = 0
        Fotherage[name] = 0
        for i in range(3, 24):
            if i <= 6:
                number = int(dist[i])
                Funder18[name] += number
            if i > 6 and i <= 9:
                number = int(dist[i])
                F19to35[name] += number
            if i > 9 and i <= 11:
                number = int(dist[i])
                F36to45[name] += number
            else:
                number = int(dist[i])
                Fotherage[name] += number


def datachanger(data):
    list_data = []
    for name in list_name:
        combine = tuple()
        combine = (name, data[name])
        list_data.append(combine)

    return list_data


def order(data):
    data = sorted(data, key=lambda x: (x[1], x[0]), reverse=True)
    return data


Funder18 = datachanger(Funder18)
F19to35 = datachanger(F19to35)
F36to45 = datachanger(F36to45)
Fotherage = datachanger(Fotherage)
Munder18 = datachanger(Munder18)
M19to35 = datachanger(M19to35)
M36to45 = datachanger(M36to45)
Motherage = datachanger(Motherage)

Funder18 = order(Funder18)
F19to35 = order(F19to35)
F36to45 = order(F36to45)
Fotherage = order(Fotherage)
Munder18 = order(Munder18)
M19to35 = order(M19to35)
M36to45 = order(M36to45)
Motherage = order(Motherage)

list_everyrange = []
list_everyrange.append(Funder18)
list_everyrange.append(F19to35)
list_everyrange.append(F36to45)
list_everyrange.append(Fotherage)
list_everyrange.append(Munder18)
list_everyrange.append(M19to35)
list_everyrange.append(M36to45)
list_everyrange.append(Motherage)
list_titles = ["    18歲以下的女性", "    19歲到35歲的女性", "    36歲到45歲的女性",
               "    46歲以上女性", "    18歲以下的男性", "    19歲到35歲的男性",
               "    36歲到45歲的男性", "    46歲以上男性"]
# 開始計算分數，以十分為滿分，按比例給分
lowerest_point = []
high_point_ad = []
list_all_adj = []
for i in range(8):
    data = list_everyrange[i]
    lowerest_point.append(data[624][1])
for i in range(8):
    data = list_everyrange[i]
    list_one_adj = []
    for k in range(len(data)):
        comb = data[k]
        list_one_adj.append(int(comb[1]) - int(lowerest_point[i]))
        if k == 0:
            high_point_ad.append(int(comb[1]) - int(lowerest_point[i]))
    list_all_adj.append(list_one_adj)
    # 以最高分者為10分，算出比例
for i in range(8):
    high_point_ad[i] = 10/int(high_point_ad[i])
list_average = []
for i in range(8):
    data = list_all_adj[i]
    list_all_adj[i][0] = 10
    average = int(10)
    for k in range(1, len(data)):
        point = int(data[k]) * float(high_point_ad[i])
        if point == float(0.0):
            point = int(0)
        list_all_adj[i][k] = round(point, 2)
        average += point
    average = round(average/625, 3)
    list_average.append(average)
print(list_average)
# 寫入檔案
result.writelines("台中市各區各年齡分數(按比例給分)\n")
result.writelines("\n")
for i in range(8):
    result.writelines(str(list_titles[i])+"\n")
    result.writelines("\n")
    for k in range(625):
        place = list_everyrange[i][k][0]
        point = round(float(list_all_adj[i][k]), 2)
        result.writelines("{:8s} : {}分\n".format(place, point))
    result.writelines("平均分數 :{}\n".format(list_average[i]))
    result.writelines("\n")
