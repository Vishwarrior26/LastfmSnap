from datetime import date, datetime
from bs4 import BeautifulSoup
from operator import itemgetter
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
        elif start == "ALL":
            self.start = "2020-08-02"
            end = "TODAY"
        if end == "NONE":
            self.end = self.start
        elif end == "TODAY":
            self.end = str(date.today())
        else:
            self.end = end
        if size != "MAX":
            self.size = int(size)
            self.pages = int(math.ceil(self.size / 50))
        else:
            self.size = None

    def __clean(self, tempinfo):
        for temp in tempinfo:
            temp[0] = temp[0].replace("&quot;", " ").lstrip(' ')
            temp[0] = temp[0].replace("&amp;", "&")
            temp[0] = temp[0].replace("/", " ")
            temp[0] = temp[0].replace(":", " ")
            if temp[0] == "永田権太":
                temp[0] = "Kenta Nagata"
            if temp[0] == "The Scorpions":
                temp[0] = "Scorpions"
            if temp[0] == "Vitalis Eirich Stephen Rippy" or temp[0] == "David Rippy, Stephen Rippy":
                temp[0] = "Stephen Rippy"
            if temp[0] == "Ludwig Göransson":
                temp[0] = "Ludwig Goransson"
            if self.type != 'artists':
                if temp[0] == "Zack Bower" or temp[0] == "The Rolling Stones" or temp[0] == "Camel":
                    temp[1] = re.sub(r" ?\([^)]+\)", "", temp[1]).lstrip(' ')
                if temp[0] == "Dire Straits" and temp[1] == " Romeo and Juliet":
                    temp[1] = "Romeo & Juliet"
                temp[1] = temp[1].replace("&amp;", "&")
                temp[1] = temp[1].replace(":", " ")
                temp[1] = temp[1].replace("?", " ")
                temp[1] = temp[1].replace("/", " ")
                temp[1] = temp[1].replace("&quot;", " ").lstrip(' ')
                if temp[1] == "The Bridge of Khazad Dum":
                    temp[1] = "The Bridge of Khazad-Dûm"
                if temp[1] == "Mary Jane's Last Dance":
                    temp[0] = "Tom Petty and The Heartbreakers"
                if temp[1] == "El Mañana":
                    temp[1] = "El Manana"
                if temp[1] == "The Monkey Book":
                    temp[1] = "Pork Parts"
                if temp[1] == "Andúril":
                    temp[1] = "Anduril"
                if temp[1] == "Main Menu" and temp[0] == "Asuka Ohta, Ryo Nagamatsu":
                    temp[1] = "Title"
                if temp[1] == "2112  I. Overture   II. The Temples of Syrinx   III. Discovery   IV. Presentation   V. Oracle  the Dream   VI. Soliloquy   VII. Grand Finale":
                    temp[1] = "2112"
                if temp[1] == "Welcome Home":
                    temp[1] = "Welcome Home (Sanitarium)"
                if temp[1] == "God's Gift":
                    temp[1] = "Gods Gift"

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
        self.__clean(test)
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

    def artistCounts(self):
        artists = []
        for temp in self.trackInfo():
            artist = temp[0]
            if artist not in (row[0] for row in artists):
                artists.append([artist, 1])
            else:
                for row in artists:
                    if row[0] == artist:
                        row[-1] += 1
        return sorted(artists, key=itemgetter(-1), reverse=True)

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


sc = scrape("100", "ALL")
# print(sc.albumInfo())
print(sc.trackInfo())
