import scrape

# sc = scrape.scrape("100", "ALL", "", "cs188")
# sc = scrape.scrape("MAX", "ALL")
# sc = scrape.scrape("2", "2022-01-01", "TODAY")
sc = scrape.scrape("MAX", "2022-01-01", "TODAY")
# print(help(sc.setUser))
# print(sc.dailyScrobbles())
# print(sc.scrobbleCounts())
print(sc.specTrackArtist("Pink Floyd"))
