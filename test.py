from operator import itemgetter
import scrape
import csv

sc = scrape.scrape("100", "ALL")
artists = []
tempinfo = sc.trackInfo()

for temp in tempinfo:
    artist = temp[0]
    if artist not in (row[0] for row in artists):
        artists.append([artist, 0])

for temper in artists:
    artist = temper[0]
    for temp in tempinfo:
        if temp[0] == artist:
            temper[-1] += 1

print(sorted(artists, key=itemgetter(-1), reverse=True))
