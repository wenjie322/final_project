import get_data as gd
result = input()
result = open(result, "w", encoding="utf8")
d_gender = gd.get_all_data("性別.json")
d_square = gd.get_all_data("面積.json")
list_dist = ["下寮里", "大村里", "大庄里", "中正里", "中和里", "文化里",
             "永安里", "永寧里", "安仁里", "南簡里", "草湳里", "頂寮里", "福德里", "興農里"]
list_male = []
list_female = []
print(d_square)
for dist in list_dist:
    male = d_gender[dist][1]
    female = d_gender[dist][2]
    sqaure = float(d_square[dist])
    mcom = (dist, male/sqaure)
    fcom = (dist, female/sqaure)
    list_male.append(mcom)
    list_female.append(fcom)
list_male = sorted(list_male, key=lambda x: (x[1], x[0]), reverse=True)
list_female = sorted(list_female, key=lambda x: (x[1], x[0]), reverse=True)
print(list_male)
male_low = float(list_male[13][1])
female_low = float(list_female[13][1])
male_adj = 10/(float(list_male[0][1])-male_low)
female_adj = 10/(float(list_female[0][1])-female_low)
print(male_adj, "male_adj")
mresult = []
fresult = []
for i in range(14):
    mdist = list_male[i][0]
    fdist = list_female[i][0]
    if i == 0:
        mcom = [mdist, 10]
        fcom = [fdist, 10]
        mresult.append(mcom)
        fresult.append(fcom)
    elif i == 13:
        mcom = [mdist, 0]
        fcom = [fdist, 0]
        mresult.append(mcom)
        fresult.append(fcom)
    else:
        mscore = (float(list_male[i][1])-male_low)*male_adj
        fscore = (float(list_female[i][1])-female_low)*female_adj
        mcom = [mdist, round(mscore, 2)]
        fcom = [fdist, round(fscore, 2)]
        mresult.append(mcom)
        fresult.append(fcom)
result.writelines("梧棲區各里男性評分"+"\n")
result.writelines(""+"\n")
for com in mresult:
    dist = com[0]
    number = com[1]
    result.writelines("{}: {}\n".format(dist, number))
result.writelines(""+"\n")
result.writelines("梧棲區各里女性評分\n")
result.writelines("\n")
for com in fresult:
    dist = com[0]
    number = com[1]
    result.writelines("{}: {}\n".format(dist, number))
print(mresult)
