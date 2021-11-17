from bs4 import BeautifulSoup
import requests
url = "https://www.last.fm/user/vishwarrior/library/artists?from=2021-11-10&to=2021-11-10"
# url = "https://www.last.fm/user/vishwarrior/library/artists?from=2020-08-01&to=2021-11-14"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
#print(soup)
description = soup.find_all("meta", property="og:description")
temp = str(description[1])
init =temp.find('"')+1
fini = temp.find('"',init+1)
# print(init)
# print(fini)
# print(temp[init:fini])
# print(temp[init:fini].split(")"))
# print(temp[init:fini].replace("(","").split(")"))
templist = temp[init:fini].replace("(","").split(")")
for i in range(1,len(templist)):
    templist[i] = templist[i][2:]
# print(templist)
del templist[-1] # check again later if necessary
# print(templist)
artists = []
plays = []
for temper in templist:
    # print(temper)
    play = temper.split(" ")[-1]
    # print(temper.find(play))
    artist = temper[:temper.find(play)-1]
    # print(len(artist))
    # print(artist)
    # print(temper.split(" "))
    # print(temper.split(" ")[-1])
    plays.append(play)
    artists.append(artist)
print(artists)
print(plays)
# print(temp)
# print(description[1])
# descriptionArray = []
# for temp in description:
#     print(temp)
#     descriptionArray.append(temp)
# print(type(description))
# print(description)
