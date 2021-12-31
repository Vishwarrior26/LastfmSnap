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

# sc = scrape(1, "2021-08-15")
# tempinfo = sc.trackInfo()[0]
# # print(tempinfo)
# path = "D:\\Music\\" + tempinfo[0] + "\\" + tempinfo[1] + ".mp3"
# # print(path)
# audio = MP3(path)
# print(audio.info.length)
# # print(round(int(audio.info.length) * int(tempinfo[2]) / 60, 3))
# print(round(int(audio.info.length) * tempinfo[2] / 60, 3))

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
