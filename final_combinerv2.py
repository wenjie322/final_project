# 此程式第一部分是用來計算最終輸出分數用，其中dict裡的數據由其他對應的scorer得到
# 第二部分為取得個別分數的函數
def writedict(thefile, dist):
    thedict = dict()
    for line in thefile:
        list_line = line.split(" ")
        key = list_line[0]
        score = list_line[1]
        if dist in key and "合計" not in key:
            thedict[key] = score.strip('\n')
    return thedict


def fin_combiner(list_rank, dist):
    import math
    # list_rank則表示排名的list,順序為人口組成、薪資、社會增加率
    # dist為區名，不是區名加上里名
    # 輸出為list中有tuple
    humanfile = open("human_mixscore", "r", encoding='utf8')
    edufile = open("edu_mixscore", "r", encoding='utf8')
    socfile = open("socinc_score", "r", encoding='utf8')
    wagefile = open("wage_score", "r", encoding="utf8")
    dict_age = writedict(humanfile, dist)
    dict_edu = writedict(edufile, dist)
    dict_socinc = writedict(socfile, dist)
    dict_wage = writedict(wagefile, dist)

    list_wage = list(dict_wage.items())

    dict_final = dict()
    list_dist = []
    for i in range(len(list_wage)):
        key = list_wage[i][0]
        list_dist.append(key)

    # 先轉換成各指標預設權重
    for i in range(3):
        rank = int(list_rank[i])
        if rank == 1:
            list_rank[i] = 1.563
        if rank == 2:
            list_rank[i] = 1.205
        if rank == 3:
            list_rank[i] = 1
    h_rate = float(list_rank[0])
    w_rate = float(list_rank[1])
    s_rate = float(list_rank[2])
    # 再處理成組合權重
    if h_rate < 1.667:
        h_rate = h_rate + (math.log(1.5*(1.667-h_rate)+1))/2
    else:
        h_rate = h_rate - (math.log(1.5*(h_rate-1.667)+1))/2
    if w_rate < 1.245:
        w_rate = w_rate + (math.log(1.5*(1.245-w_rate)+1))/2
    else:
        w_rate = w_rate - (math.log(1.5*(w_rate-1.245)+1))/2
    s_rate = s_rate - (math.log(1.5*(s_rate-1)+1))/2
    print(h_rate, w_rate, s_rate)
    # 計算開始
    for i in range(len(list_dist)):
        dist = list_dist[i]
        age = float(dict_age[dist])
        edu = float(dict_edu[dist])
        socnic = float(dict_socinc[dist])
        wage = float(dict_wage[dist])
        human = age/2+edu/2
        com = (human*h_rate+wage*w_rate+socnic*s_rate)/(h_rate+s_rate+w_rate)
        dict_final[dist] = round(com, 2)

    dict_final = sorted(list(dict_final.items()),
                        key=lambda y: y[1], reverse=True)

    return dict_final
# 函數fin_combiner到此結束


def fin_express(type, list_rank, dist):
    # type 輸入human,socinc或wage。個別代表人口組成、社會增加率、平均薪資。
    # list_rank則表示排名的list,順序為人口組成、薪資、社會增加率
    # 輸出為dict
    import math
    humanfile = open("human_mixscore", "r", encoding='utf8')
    edufile = open("edu_mixscore", "r", encoding='utf8')
    socfile = open("socinc_score", "r", encoding='utf8')
    wagefile = open("wage_score", "r", encoding="utf8")
    dict_human = writedict(humanfile, dist)
    dict_edu = writedict(edufile, dist)
    dict_socinc = writedict(socfile, dist)
    dict_wage = writedict(wagefile, dist)
    list_wage = list(dict_wage.items())
    dict_final = dict()
    list_dist = []
    for i in range(len(list_wage)):
        key = list_wage[i][0]
        list_dist.append(key)

    # 先轉換成各指標預設權重。預設人口組成1.734 平均所得1.228 人口消長1
    for i in range(3):
        rank = int(list_rank[i])
        if rank == 1:
            list_rank[i] = 1.992
        if rank == 2:
            list_rank[i] = 1.35
        if rank == 3:
            list_rank[i] = 1
    h_rate = float(list_rank[0])
    w_rate = float(list_rank[1])
    s_rate = float(list_rank[2])
    # 再處理成組合權重。自定義排序一1.992 平均所得1.35 人口消長1
    if h_rate < 1.734:
        h_rate = h_rate + (math.log(1.734-h_rate+1))/2
    else:
        h_rate = h_rate - (math.log(h_rate-1.734+1))/2
    if w_rate < 1.35:
        w_rate = w_rate + (math.log(1.35-w_rate+1))/2
    else:
        w_rate = w_rate - (math.log(w_rate-1.35+1))/2
    s_rate = s_rate + (math.log(s_rate))/2

    if type == "human":
        for i in range(len(list_dist)):
            dist = list_dist[i]
            age = float(dict_human[dist])
            edu = float(dict_edu[dist])

            human = age/2+edu/2
            dict_final[dist] = round((human*h_rate)/(h_rate+s_rate+w_rate), 2)
    elif type == "wage":
        for i in range(len(list_dist)):
            dist = list_dist[i]
            wage = float(dict_wage[dist])
            dict_final[dist] = round((wage*w_rate)/(h_rate+s_rate+w_rate), 2)
    elif type == "socinc":
        for i in range(len(list_dist)):
            dist = list_dist[i]
            socinc = float(dict_socinc[dist])
            dict_final[dist] = round((socinc*s_rate)/(h_rate+s_rate+w_rate), 2)

    return dict_final
# fin_express 到此結束


def final_rank(list_rank, dist):

    a = str(list_rank[0])
    b = str(list_rank[1])
    c = str(list_rank[2])

    # remain = [list_rank[0], list_rank[1], list_rank[]]

    first = fin_combiner(list_rank, dist)[0][0]
    list_rank = [int(a), int(b), int(c)]
    second = fin_combiner(list_rank, dist)[1][0]
    list_rank = [int(a), int(b), int(c)]
    third = fin_combiner(list_rank, dist)[2][0]
    list_rank = [int(a), int(b), int(c)]

    human_type = fin_express('human', list_rank, dist)
    list_rank = [int(a), int(b), int(c)]
    wage_type = fin_express('wage', list_rank, dist)
    list_rank = [int(a), int(b), int(c)]
    socinc_type = fin_express('socinc', list_rank, dist)
    list_rank = [int(a), int(b), int(c)]

    set1 = [first, human_type[first], wage_type[first], socinc_type[first]]
    set2 = [second, human_type[second], wage_type[second], socinc_type[second]]
    set3 = [third, human_type[third], wage_type[third], socinc_type[third]]
    rank_list = [set1, set2, set3]
    return rank_list


# 以下為測試用數據
test = final_rank([1, 2, 3], "北屯區")
print(test)
