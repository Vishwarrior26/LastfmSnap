from datetime import date, datetime
from bs4 import BeautifulSoup
from operator import itemgetter
import pandas as pd
import math
import requests
import re


class scrape:
    # Change var names to conform to snake_case
    """" This is the constructor docstring """

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
        for info in tempinfo:
            info[0] = info[0].replace("&quot;", " ").lstrip(' ')
            info[0] = info[0].replace("&amp;", "&")
            info[0] = info[0].replace("/", " ")
            info[0] = info[0].replace(":", " ")
            if info[0] == "永田権太":
                info[0] = "Kenta Nagata"
            if info[0] == "The Scorpions":
                info[0] = "Scorpions"
            if info[0] == "Vitalis Eirich Stephen Rippy" or info[0] == "David Rippy, Stephen Rippy":
                info[0] = "Stephen Rippy"
            if info[0] == "Ludwig Göransson":
                info[0] = "Ludwig Goransson"
            if info[0] == "Zack Bower" or info[0] == "The Rolling Stones" or info[0] == "Camel":
                info[-2] = re.sub(r" ?\([^)]+\)", "", info[-2]).lstrip(' ')
            if info[0] == "Dire Straits" and info[-2] == " Romeo and Juliet":
                info[-2] = "Romeo & Juliet"
            info[-2] = info[-2].replace("&amp;", "&")
            info[-2] = info[-2].replace(":", " ")
            info[-2] = info[-2].replace("?", " ")
            info[-2] = info[-2].replace("/", " ")
            info[-2] = info[-2].replace("&quot;", " ").lstrip(' ')
            if info[-2] == "The Bridge of Khazad Dum":
                info[-2] = "The Bridge of Khazad-Dûm"
            if info[-2] == "Mary Jane's Last Dance":
                info[0] = "Tom Petty and The Heartbreakers"
            if info[-2] == "El Mañana":
                info[-2] = "El Manana"
            if info[-2] == "The Monkey Book":
                info[-2] = "Pork Parts"
            if info[-2] == "Andúril":
                info[-2] = "Anduril"
            if info[-2] == "Main Menu" and info[0] == "Asuka Ohta, Ryo Nagamatsu":
                info[-2] = "Title"
            if info[-2] == "2112  I. Overture   II. The Temples of Syrinx   III. Discovery   IV. Presentation   V. Oracle  the Dream   VI. Soliloquy   VII. Grand Finale":
                info[-2] = "2112"
            if info[-2] == "Welcome Home":
                info[-2] = "Welcome Home (Sanitarium)"
            if info[-2] == "God's Gift":
                info[-2] = "Gods Gift"

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
        info = []
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
                        info.append([artist, kind, play])
                    else:
                        info.append([unsplit, play])
        self.__clean(info)
        return info[:self.size]

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
