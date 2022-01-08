from operator import itemgetter
import scrape
import csv

sc = scrape.scrape("100", "ALL")
# artists = []
# tempinfo = sc.trackInfo()
#
# for temp in tempinfo:
#     artist = temp[0]
#     if artist not in (row[0] for row in artists):
#         artists.append([artist, 1])
#     else:
#         for row in artists:
#             if row[0] == artist:
#                 row[-1] += 1
#
# print(sorted(artists, key=itemgetter(-1), reverse=True))

print(sc.artistCounts())
