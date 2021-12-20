from datetime import date, datetime
from bs4 import BeautifulSoup
import pandas as pd
import math
import requests
import csv


class scrape:
    #  Change var names to conform to snake_case
    # Remove type from constructor?
    def __init__(self, size=50, start="TODAY", end="NONE"):
        self.start = start
        if start == "TODAY":
            self.start = str(date.today())
        if end == "NONE":
            self.end = self.start
        elif end == "TODAY":
            self.end = str(date.today())
        else:
            self.end = end
        self.size = size
        self.pages = int(math.ceil(self.size / 50))

    def __info(self):
        urls = [self.url]
        for x in range(2, self.pages + 1):
            urls.append(self.url + "&page=" + str(x))
        test = []
        for tempUrl in urls:
            req = requests.get(tempUrl)
            soup = BeautifulSoup(req.text, "html.parser")
            description = soup.find_all("meta", property="og:description")
            if len(description) > 1:
                temp = str(description[1])
                init = temp.find('"') + 1
                fini = temp.find('"', init + 1)
                templist = temp[init:fini].split("), ")
                templist[-1] = templist[-1][:-1]
                for temper in templist:
                    play = temper.split(" ")[-1][1:]
                    unsplit = temper[:temper.find(play) - 2]
                    if self.type != 'artists':
                        splitter = unsplit.find('—')
                        artist = unsplit[:splitter - 1]
                        kind = unsplit[splitter + 2:]
                        test.append([artist, kind, play])
                    else:
                        test.append([unsplit, play])
        return test[:self.size]

    def setSize(self, size):
        self.size = size
        self.pages = int(math.ceil(self.size / 50))

    def setTime(self, start, end="NONE"):
        self.start = start
        if end == "NONE":
            self.end = start
        else:
            self.end = end

    def artistInfo(self):
        self.type = 'artists'
        self.url = "https://www.last.fm/user/vishwarrior/library/artists?from=" + \
            str(self.start) + "&to=" + str(self.end)
        return self.__info()

    def albumInfo(self):
        self.type = 'albums'
        self.url = "https://www.last.fm/user/vishwarrior/library/albums?from=" + \
            str(self.start) + "&to=" + str(self.end)
        return self.__info()

    def trackInfo(self):
        self.type = 'tracks'
        self.url = "https://www.last.fm/user/vishwarrior/library/tracks?from=" + \
            str(self.start) + "&to=" + str(self.end)
        return self.__info()


# sc = scrape()
# sc = scrape(1, "2021-04-10")
# sc = scrape(25, "2021-01-01", "TODAY")
# print(sc.artistInfo())
# print(sc.albumInfo())
# print(sc.trackInfo())

# print(sc.artistInfo())

# sc = scrape(1, "2020-04-10")
# fields = ["Arist", "Playcount"]
# with open("TopArtistDaily.csv", 'w') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(fields)
#     for day in pd.date_range(start="2020-08-02", end="2021-12-20"):
#         curday = str(day.date())
#         print(curday)
#         sc.setTime(curday)
#         csvwriter.writerows(sc.artistInfo())

# sc = scrape(50, "2020-08-02")
# file1 = open("DailyAugust2020Artists.txt", "w")
#
# for day in pd.date_range(start="2020-08-02", end="2020-08-31"):
#     curday = str(day.date())
#     sc.setTime(curday)
#     file1.write(curday)
#     file1.write("\n")
#     file1.writelines("\n".join(str(x) for x in sc.artistInfo()))
#     file1.write("\n")
# file1.close()

# for y in range(3):
#     for x in sc.trackInfo():
#         print(x[y])
#     print()
