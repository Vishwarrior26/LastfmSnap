from mutagen.mp3 import MP3
from datetime import date, datetime
from bs4 import BeautifulSoup
import pandas as pd
import math
import requests
import csv
import re


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
        self.url = "https://www.last.fm/user/vishwarrior/library/" + \
            self.type + "?from=" + (self.start) + "&to=" + str(self.end)
        # print(self.url)
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
                    play = int(temper.split(" ")[-1][1:])
                    unsplit = temper[:temper.find(str(play)) - 2]
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
        return self.__info()

    def albumInfo(self):
        self.type = 'albums'
        return self.__info()

    def trackInfo(self):
        self.type = 'tracks'
        return self.__info()

    def scrobblesInfo(self):
        self.url = "https://www.last.fm/user/vishwarrior/library?from=" + \
            str(self.start) + "&to=" + str(self.end)
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, "html.parser")
        description = soup.find_all(class_="metadata-display")
        if len(description) > 0:
            temp = str(description[0])
            # swap to extract using regex?
            # self.total = temp[temp.find(">") + 1:temp.find("<", 1)]
            self.total = int("".join(str(x) for x in re.findall(
                "[0-9]", temp[temp.find(">") + 1:temp.find("<", 1)])))
            return self.total


# sc = scrape()
# sc = scrape(1, "2021-11-01", "2021-11-30")
# sc = scrape(1, "2021-04-10")
# sc = scrape(25, "2021-01-01", "TODAY")
# print(sc.artistInfo())
# print(sc.albumInfo())
# print(sc.trackInfo())
# print(sc.scrobblesInfo())
# total = int("".join(str(x) for x in re.findall("[0-9]", sc.scrobblesInfo())))
# print(total)

sc = scrape(1, "2021-08-15")
tempinfo = sc.trackInfo()[0]
# print(tempinfo)
path = "D:\\Music\\" + tempinfo[0] + "\\" + tempinfo[1] + ".mp3"
# print(path)
audio = MP3(path)
print(audio.info.length)
# print(round(int(audio.info.length) * int(tempinfo[2]) / 60, 3))
print(round(int(audio.info.length) * tempinfo[2] / 60, 3))
# fields = ["Tracks", "Plays"]
# sc = scrape(50, "2020-08-02", "TODAY")
# with open("AllTimeTopTracks.csv", 'w') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(fields)
#     csvwriter.writerows(sc.trackInfo())

# sc = scrape(1, "2020-04-10")
# fields = ["Date", "Plays"]
# with open("PlaysPerDay.csv", 'w') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(fields)
#     # for day in pd.date_range(start="2020-08-02", end="2020-08-10"):
#     for day in pd.date_range(start="2020-08-02", end="2021-12-20"):
#         curday = str(day.date())
#         print(curday)
#         sc.setTime(curday)
#         csvwriter.writerow([curday, sc.scrobblesInfo()])

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
