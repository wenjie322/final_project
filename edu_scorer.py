import get_data as gd
result = input()
result = open(result, "w", encoding="utf8")
d_educ = gd.get_all_data("教育程度.json")
d_square = {"下寮里": 0.3275, "大村里": 1.3775, "大庄里": 1.4125, "中正里": 0.2100, "中和里": 0.0954, "文化里": 0.1925,
            "永安里": 1.6575, "永寧里": 1.6275, "安仁里": 0.1325, "南簡里": 1.8750, "草湳里": 3.3175, "頂寮里": 0.8675, "福德里": 1.4995, "興農里": 2.0125}

list_dist = ["下寮里", "大村里", "大庄里", "中正里", "中和里", "文化里",
             "永安里", "永寧里", "安仁里", "南簡里", "草湳里", "頂寮里", "福德里", "興農里"]

d_a = gd.get_data_by_neighborhood("面積.json", "面積")

list_gra = []
list_college = []
list_high = []
list_elem = []
ttrate = float()
for dist in list_dist:
    rate = d_square[dist]
    edu = d_educ[dist]
    gra_num = int()
    col_num = int()
    hig_num = int()
    ele_num = int()

    for i in range(13):
        sedu = edu[i]
        if i <= 1:
            gra_num += int(sedu)
        if i >= 2 and i <= 4:
            col_num += int(sedu)
        if i >= 5 and i <= 8:
            hig_num += int(sedu)
        if i >= 9 and i <= 10:
            ele_num += int(sedu)

    com = (dist, sedu/rate)
    list_elem.append(com)
    ttrate += round(rate, 2)
    com = (dist, col_num/rate)
    list_college.append(com)
    com = (dist, hig_num/rate)
    list_high.append(com)
    com = (dist, gra_num/rate)
    list_gra.append(com)


def order(data):
    data = sorted(data, key=lambda x: (x[1], x[0]), reverse=True)
    return data


list_all = []
list_college = order(list_college)
list_elem = order(list_elem)
list_gra = order(list_gra)
list_high = order(list_high)

list_all.append(list_gra)
list_all.append(list_college)
list_all.append(list_high)
list_all.append(list_elem)


list_adj = []
count = int(1)
for level in list_all:
    list_single = []
    edu_low = level[13][1]
    edu_adj = (5-count)/(float(level[0][1])-edu_low)
    for i in range(14):
        dist = level[i][0]
        score = round(float(level[i][1])*edu_adj, 2)
        if i == 0:
            score = 5-count
        com = [dist, score]
        list_single.append(com)
    count += 1
    list_adj.append(list_single)

list_fin = []
for i in range(14):
    total = float()
    dist = list_adj[0][i][0]
    for k in range(4):
        total += float(list_adj[k][i][1])
    total = round(total, 2)
    list_fin.append((dist, total))
result.writelines("台中市梧棲區教育程度分數\n")
result.writelines("\n")
for com in list_fin:
    result.writelines("{}: {}分\n".format(com[0], com[1]))
