# 本程式用於將經緯度轉換成精確的地址資料。 今晚搞定，明天睡到自然醒
from geopy.geocoders import Nominatim
import time
thefile = open("new_temple_latlng.txt", "r", encoding="utf8")
result = open("final_temple", "a", encoding="utf8")
re_search = open("temple_re_search", "a", encoding='utf8')


for line in thefile:
    if "臺中" in line and "/" in line:
        newline = line.replace("/", "")
        list_line = newline.split(" ")
        latlng = list_line[2]
        latlng = latlng.replace(",", ", ")

        geolocator = Nominatim(user_agent="fate")
        location = geolocator.reverse(
            latlng, timeout=10)
        try:
            village = location.raw["address"]["neighbourhood"]

            location = list_line[1]
            insert = location.find("區")
            location = location[:insert+1]+village+location[insert+1:]
            list_line[1] = location
            print(location)
            print(list_line)
            for i in range(len(list_line)):
                if i >= int(len(list_line))-1:
                    result.writelines(list_line[i])
                else:
                    result.writelines(list_line[i]+" ")
        except:
            print("alert", list_line)
            for i in range(len(list_line)):
                if i >= int(len(list_line))-1:
                    result.writelines(list_line[i])
                else:
                    result.writelines(list_line[i]+" ")
            for i in range(len(list_line)):
                if i >= int(len(list_line))-1:
                    re_search.writelines(list_line[i])
                else:
                    re_search.writelines(list_line[i]+" ")
    else:
        if line != "/n":
            list_line = line.split(" ")
            for i in range(len(list_line)):
                if i >= int(len(list_line))-1:
                    result.writelines(list_line[i])
                else:
                    result.writelines(list_line[i]+" ")
