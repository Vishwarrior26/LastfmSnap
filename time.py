from operator import itemgetter
from mutagen.mp3 import MP3
import scrape
import csv
import pandas as pd
import math
import re

# sc = scrape.scrape("MAX", "2020-08-02", "TODAY")
# fields = ["Artist", "Tracks", "Plays"]
# with open("TopTracksWithTime.csv", 'w', encoding='utf-8',  newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(fields)
#     csvwriter.writerows(sc.trackInfo())

# sc = scrape.scrape("MAX", "2020-08-02", "TODAY")
# tempinfo = sc.trackInfo

tempinfo = []
with open("TopTracksWithTime.csv", 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        tempinfo.append(row)
Artists = []
for temp in tempinfo[1:]:
    artist = temp[0]
    track = temp[1]
    plays = int(temp[2])
    artist = artist.replace("&quot;", " ").lstrip(' ')
    artist = artist.replace("&amp;", "&")
    artist = artist.replace("/", " ")
    artist = artist.replace(":", " ")
    track = track.replace("&amp;", "&")
    track = track.replace(":", " ")
    track = track.replace("?", " ")
    track = track.replace("/", " ")
    track = track.replace("&quot;", " ").lstrip(' ')
    if artist == "Zack Bower" or artist == "The Rolling Stones" or artist == "Camel":
        track = re.sub(r" ?\([^)]+\)", "", track).lstrip(' ')
    if artist == "永田権太":
        artist = "Kenta Nagata"
    if artist == "The Scorpions":
        artist = "Scorpions"
    if artist == "Vitalis Eirich Stephen Rippy" or artist == "David Rippy, Stephen Rippy":
        artist = "Stephen Rippy"
    if artist == "Ludwig Göransson":
        artist = "Ludwig Goransson"
    if artist == "Dire Straits" and track == " Romeo and Juliet":
        track = "Romeo & Juliet"
    if track == "The UTULEK Complex Golem City":
        track = "The UTULEK Complex  Golem City"
    if track == "The Bridge of Khazad Dum":
        track = "The Bridge of Khazad-Dûm"
    if track == "Mary Jane's Last Dance":
        artist = "Tom Petty and The Heartbreakers"
    if track == "El Mañana":
        track = "El Manana"
    if track == "The Monkey Book":
        track = "Pork Parts"
    if track == "Andúril":
        track = "Anduril"
    if track == "Main Menu" and artist == "Asuka Ohta, Ryo Nagamatsu":
        track = "Title"
    if track == "2112  I. Overture   II. The Temples of Syrinx   III. Discovery   IV. Presentation   V. Oracle  the Dream   VI. Soliloquy   VII. Grand Finale":
        track = "2112"
    if track == "Welcome Home":
        track = "Welcome Home (Sanitarium)"
    if track == "God's Gift":
        track = "Gods Gift"
    path = "D:\\Music\\" + artist + "\\" + track + ".mp3"
    if artist not in (row[0] for row in Artists):
        Artists.append([artist, 0, 0])
    if path == "D:\\Music\\Dire Straits\\The Man’s Too Strong.mp3":
        path = "D:\Music\Dire Straits\The Man's Too Strong.mp3"
    try:
        audio = MP3(path)
        temp.append(round(int(audio.info.length) * plays / 60, 3))
    except:
        tempinfo.remove(temp)
print(tempinfo)
fields = ["Artist", "Tracks", "Plays", "Time"]
with open("TopTracksWithTime1.csv", 'w', encoding='utf-8',  newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(sorted(tempinfo[1:], key=itemgetter(3), reverse=True))

for temper in Artists:
    artist = temper[0]
    for temp in tempinfo:
        if temp[0] == artist:
            temper[1] += int(temp[2])
            temper[2] += int(temp[3])

print(sorted(Artists, key=itemgetter(2), reverse=True))
print(sorted(Artists, key=itemgetter(1), reverse=True))

# fields = ["Artist", "Tracks", "Plays", "Time"]
# with open("TrackTotalTimes.csv", 'w', encoding='utf-8',  newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(fields)
#     csvwriter.writerows(tempinfo)
