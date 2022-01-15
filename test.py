import scrape

sc = scrape.scrape("100", "ALL")
# sc = scrape.scrape("MAX", "ALL")
# sc = scrape.scrape("1", "2022-01-01", "TODAY")
# sc = scrape.scrape("MAX", "2022-01-01", "TODAY")
# print(help(sc.setUser))
# print(sc.dailyScrobbles())
# print(sc.dailyTracks())
# print(sc.scrobbleCounts())
print(sc.specTrackArtist("Tool", False))
