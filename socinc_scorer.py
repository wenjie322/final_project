import get_data as gd
result = input()
result = open(result, "w", encoding="utf8")
d_soc_inc = gd.get_all_data("社會增加.json")
list_dist = ["下寮里", "大村里", "大庄里", "中正里", "中和里", "文化里",
             "永安里", "永寧里", "安仁里", "南簡里", "草湳里", "頂寮里", "福德里", "興農里"]
list_rate = []
for dist in list_dist:
    rate = d_soc_inc[dist][3]
    list_rate.append((dist, rate))
list_rate = sorted(list_rate, key=lambda x: (float(x[1]), x[0]), reverse=True)

rresult = []
rate_low = float(list_rate[13][1])
rate_adj = 10/(float(list_rate[0][1])-rate_low)
for i in range(14):
    dist = list_rate[i][0]
    rate = float(list_rate[i][1])
    if i == 0:
        com = [dist, 10]
    elif i == 13:
        com = [dist, 0]
    elif rate < 0:
        com = [dist, 0]
    else:
        score = (float(rate)-rate_low)*rate_adj
        com = [dist, score]
    rresult.append(com)
result.writelines("梧棲區社會增加率分數\n")
result.writelines("\n")
for com in rresult:
    dist = com[0]
    score = com[1]
    result.writelines("{}: {}\n".format(dist, round(score, 2)))
