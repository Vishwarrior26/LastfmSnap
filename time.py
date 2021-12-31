from mutagen.mp3 import MP3
import scrape
import csv
# sc = scrape.scrape(10, "2021-08-15", "TODAY")
sc = scrape.scrape("MAX", "2020-08-02", "TODAY")
# print(sc.artistInfo())
print("Writing to CSV")
fields = ["Tracks", "Plays", "Time"]
with open("TopTracksWithTime.csv", 'w', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(sc.trackInfo())
# tempinfo = sc.trackInfo()
# print(tempinfo)
# for temp in tempinfo:
#     artist = temp[0]
#     track = temp[1]
#     plays = temp[2]
#     artist = artist.replace("&quot;", " ").lstrip(' ')
#     track = track.replace(":", " ")
#     path = "D:\\Music\\" + artist + "\\" + track + ".mp3"
#     print(path)
#     audio = MP3(path)
#     # print(round(int(audio.info.length) * plays / 60, 3))
#     temp.append(round(int(audio.info.length) * plays / 60, 3))
# print(tempinfo)
