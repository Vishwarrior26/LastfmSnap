from bs4 import BeautifulSoup
import requests


class scrape:

    def __init__(self, type, start, end):
        self.start = start
        self.end = end
        self.type = type

    def __info(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")
        description = soup.find_all("meta", property="og:description")
        temp = str(description[1])
        init = temp.find('"') + 1
        fini = temp.find('"', init + 1)
        templist = temp[init:fini].replace("(", "").split(")")
        for i in range(1, len(templist)):
            templist[i] = templist[i][2:]
        del templist[-1]
        test = []
        for temper in templist:
            play = temper.split(" ")[-1]
            type = temper[:temper.find(play) - 1]
            test.append([type, play])
        return test

    def artistInfo(self):
        self.url = "https://www.last.fm/user/vishwarrior/library/artists?from=" + \
            str(self.start) + "&to=" + str(self.end)
        return self.__info()

    def albumInfo(self):
        self.url = "https://www.last.fm/user/vishwarrior/library/albums?from=" + \
            str(self.start) + "&to=" + str(self.end)
        return self.__info()

    def trackInfo(self):
        self.url = "https://www.last.fm/user/vishwarrior/library/tracks?from=" + str(self.start) + "&to=" + str(self.end)
        return self.__info()


sc = scrape("tracks", "2021-09-01", "2021-09-30")
print(sc.artistInfo())
print(sc.albumInfo())
print(sc.trackInfo())
