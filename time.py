from mutagen.mp3 import MP3
import scrape

sc = scrape.scrape(1, "2021-08-15")
tempinfo = sc.trackInfo()[0]
# print(tempinfo)
path = "D:\\Music\\" + tempinfo[0] + "\\" + tempinfo[1] + ".mp3"
# print(path)
audio = MP3(path)
print(audio.info.length)
# print(round(int(audio.info.length) * int(tempinfo[2]) / 60, 3))
print(round(int(audio.info.length) * tempinfo[2] / 60, 3))
