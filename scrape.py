from bs4 import BeautifulSoup
import requests


class scrape:
    def __init__(self, url):
        self.url = url

    def getInfo(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")
        description = soup.find_all("meta", property="og:description")
        temp = str(description[1])
        init = temp.find('"') + 1
        fini = temp.find('"', init + 1)
        templist = temp[init:fini].replace("(", "").split(")")
        for i in range(1, len(templist)):
            templist[i] = templist[i][2:]
        del templist[-1]  # check again later if necessary
        artists = []
        plays = []
        test = []
        for temper in templist:
            play = temper.split(" ")[-1]
            artist = temper[:temper.find(play) - 1]
            plays.append(play)
            artists.append(artist)
            test.append([artist, play])
        return test
