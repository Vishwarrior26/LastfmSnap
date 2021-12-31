from datetime import date, datetime
from bs4 import BeautifulSoup
import pandas as pd
import math
import requests
import re


class scrape:
    # Change var names to conform to snake_case
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
        if size != "MAX":
            self.size = size
            self.pages = int(math.ceil(self.size / 50))
        else:
            self.size = None

    def __info(self):
        self.url = "https://www.last.fm/user/vishwarrior/library/" + \
            self.type + "?from=" + (self.start) + "&to=" + str(self.end)
        # print(self.url)
        urls = [self.url]
        if self.size is None:
            req = requests.get(self.url)
            soup = BeautifulSoup(req.text, "html.parser")
            description = soup.find_all(class_="pagination-page")
            self.pages = int(re.findall('[0-9]+', str(description[-1]))[-1])
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
