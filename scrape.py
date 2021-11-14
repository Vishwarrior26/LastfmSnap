from bs4 import BeautifulSoup
import requests
url = "https://www.last.fm/user/vishwarrior/library/artists?from=2021-11-10&to=2021-11-10"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
description = soup.find_all("meta", property="og:description")
temp = str(description[1])
init =temp.find('"')+1
fini = temp.find('"',init+1)
templist = temp[init:fini].replace("(","").split(")")
for i in range(1,len(templist)):
    templist[i] = templist[i][2:]
del templist[-1] # check again later if necessary
artists = []
plays = []
for temper in templist:
    play = temper.split(" ")[-1]
    artist = temper[:temper.find(play)-1]
    plays.append(play)
    artists.append(artist)
