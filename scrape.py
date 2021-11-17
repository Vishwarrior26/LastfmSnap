from bs4 import BeautifulSoup
import requests


class scrape:

    def __init__(self, type, start, end="NONE", size=0):
        self.start = start
        if end == "NONE":
            self.end = start
        else:
            self.end = end
        self.type = type
        self.size = size

    def __info(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")
        description = soup.find_all("meta", property="og:description")
        temp = str(description[1])
        init = temp.find('"') + 1
        fini = temp.find('"', init + 1)
        templist = temp[init:fini].split("), ")
        del templist[-1]
        test = []
        # maybe split artist for albums and tracks into another entry? eg (artist, album/track, count)
        for temper in templist:
            play = temper.split(" ")[-1][1:]
            type = temper[:temper.find(play) - 2]
            test.append([type, play])
        if self.size == 0:
            self.size = len(test)
        return test[:self.size]

    def setSize(self, size):
        self.size = size

    def setTime(self, start, end="NONE"):
        self.start = start
        if end == "NONE":
            self.end = start
        else:
            self.end = end

    def artistInfo(self):
        self.url = "https://www.last.fm/user/vishwarrior/library/artists?from=" + \
            str(self.start) + "&to=" + str(self.end)
        return self.__info()

    def albumInfo(self):
        self.url = "https://www.last.fm/user/vishwarrior/library/albums?from=" + \
            str(self.start) + "&to=" + str(self.end)
        return self.__info()

    def trackInfo(self):
        self.url = "https://www.last.fm/user/vishwarrior/library/tracks?from=" + \
            str(self.start) + "&to=" + str(self.end)
        return self.__info()

# sc = scrape("album", "2020-08-01", "2021-11-16",4)
# sc = scrape("album", "2021-11-16", "NONE")
# print(sc.artistInfo())
# print(sc.albumInfo())
# print(sc.trackInfo())


sc = scrape("album", "2021-10-01", "NONE", 1)
startdate = "2021-10-01"

while int(startdate[-2:]) < 32:
    print("startdate " + startdate)
    print(sc.trackInfo())
    end = int(startdate[-2:]) + 1
    if(end<10):
        end = "0" + str(end)
    print("end " + end)
    print("new startdate " + startdate[:7] + str(end))
    sc.setTime(startdate[:7] + str(end))
