from datetime import date, datetime
from bs4 import BeautifulSoup
from operator import itemgetter
import pandas as pd
import math
import requests
import re


class scrape:
    # Change var names to conform to snake_case
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
            if temp[0] == "Zack Bower" or temp[0] == "The Rolling Stones" or temp[0] == "Camel":
                temp[-2] = re.sub(r" ?\([^)]+\)", "", temp[-2]).lstrip(' ')
            if temp[0] == "Dire Straits" and temp[-2] == " Romeo and Juliet":
                temp[-2] = "Romeo & Juliet"
            temp[-2] = temp[-2].replace("&amp;", "&")
            temp[-2] = temp[-2].replace(":", " ")
            temp[-2] = temp[-2].replace("?", " ")
            temp[-2] = temp[-2].replace("/", " ")
            temp[-2] = temp[-2].replace("&quot;", " ").lstrip(' ')
            if temp[-2] == "The Bridge of Khazad Dum":
                temp[-2] = "The Bridge of Khazad-Dûm"
            if temp[-2] == "Mary Jane's Last Dance":
                temp[0] = "Tom Petty and The Heartbreakers"
            if temp[-2] == "El Mañana":
                temp[-2] = "El Manana"
            if temp[-2] == "The Monkey Book":
                temp[-2] = "Pork Parts"
            if temp[-2] == "Andúril":
                temp[-2] = "Anduril"
            if temp[-2] == "Main Menu" and temp[0] == "Asuka Ohta, Ryo Nagamatsu":
                temp[-2] = "Title"
            if temp[-2] == "2112  I. Overture   II. The Temples of Syrinx   III. Discovery   IV. Presentation   V. Oracle  the Dream   VI. Soliloquy   VII. Grand Finale":
                temp[-2] = "2112"
            if temp[-2] == "Welcome Home":
                temp[-2] = "Welcome Home (Sanitarium)"
            if temp[-2] == "God's Gift":
                temp[-2] = "Gods Gift"

    def __info(self):
        self.url = "https://www.last.fm/user/vishwarrior/library/" + \
            self.type + "?from=" + (self.start) + "&to=" + str(self.end)
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
            self.total = int("".join(str(x) for x in re.findall(
                "[0-9]", temp[temp.find(">") + 1:temp.find("<", 1)])))
            return self.total
