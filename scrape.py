from bs4 import BeautifulSoup
import requests


class scrape:

    def __init__(self, type, start, end="start"):
        if end == "start":
            end = start
        self.start = start
        self.end = end
        self.url = "https://www.last.fm/user/vishwarrior/library/" + type + "?from=" + \
            str(start) + "&to=" + str(end)

    def __setType(self, type):
        self.url = "https://www.last.fm/user/vishwarrior/library/" + type + "?from=" + \
            str(self.start) + "&to=" + str(self.end)

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
        del templist[-1]  # check again later if necessary
        test = []
        for temper in templist:
            play = temper.split(" ")[-1]
            type = temper[:temper.find(play) - 1]
            test.append([type, play])
        return test

    def artistInfo(self):
        self.__setType("artists")
        return self.__info()

    def albumInfo(self):
        self.__setType("albums")
        return self.__info()

    def trackInfo(self):
        self.__setType("tracks")
        return self.__info()


sc = scrape("tracks", "2021-09-01", "2021-09-30")
print(sc.artistInfo())
print(sc.albumInfo())
print(sc.trackInfo())
