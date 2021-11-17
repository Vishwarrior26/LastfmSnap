from bs4 import BeautifulSoup
import requests


class scrape:

    def __init__(self, type, start="None", end="None"):
        if start == "None" and end == "None":
            self.url = "https://www.last.fm/user/vishwarrior/library/"+ type + "?date_preset=ALL"
        elif end == "None":
            end = start
            self.url = "https://www.last.fm/user/vishwarrior/library/" + type + "?from=" + \
                str(start) + "&to=" + str(end)
        else:
            self.url = "https://www.last.fm/user/vishwarrior/library/" + type + "?from=" + \
                str(start) + "&to=" + str(end)
        self.start = start
        self.end = end
        self.type = type


    def __setType(self, type):
        print(self.url)
        print(self.type)
        print(type)
        self.url = self.url.replace(self.type, type)
        print(self.url)


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
        self.__setType("artists")
        return self.__info()

    def albumInfo(self):
        self.__setType("albums")
        return self.__info()

    def trackInfo(self):
        self.__setType("tracks")
        return self.__info()


sc = scrape("tracks", "2021-09-01", "2021-09-30")
# sc = scrape("artists")
print(sc.artistInfo())
print(sc.albumInfo())
print(sc.trackInfo())
