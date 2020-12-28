import get_data as gd
result = input()
result = open(result, "w", encoding="utf8")
d_wage = gd.get_all_data("所得.json")
list_dist = ["下寮里", "大村里", "大庄里", "中正里", "中和里", "文化里",
             "永安里", "永寧里", "安仁里", "南簡里", "草湳里", "頂寮里", "福德里", "興農里"]
list_allwage = []
for dist in list_dist:
    list_allwage.append((dist, d_wage[dist][2]))
list_allwage = sorted(list_allwage, key=lambda x: (x[1], x[0]), reverse=True)
wage_low = float(list_allwage[13][1])
wage_adj = 10/(float(list_allwage[0][1])-wage_low)
list_rank = []
for i in range(14):
    com = list_allwage[i]
    wage = (float(com[1])-wage_low)*wage_adj
    dist = com[0]
    if i == 0:
        comb = [dist, 10]
    elif i == 13:
        comb = [dist, 0]
    else:
        comb = [dist, wage]
    list_rank.append(comb)
result.writelines("梧棲區平均月薪分數\n")
result.writelines("\n")
for com in list_rank:
    dist = com[0]
    score = com[1]
    result.writelines("{}: {}\n".format(dist, round(score, 2)))
