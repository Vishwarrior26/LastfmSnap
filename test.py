import scrape

# sc = scrape.scrape("100", "ALL", "", "cs188")
# print(sc.scrobblesInfo())
# sc = scrape.scrape("100", "ALL")
# print(sc.scrobblesInfo())

sc = scrape.scrape("2", "2022-01-01", "TODAY")
# print(sc.dailyArtists())
# print(sc.dailyAlbums())
# print(sc.dailyTracks())
for x in sc.dailyTracks():
    print(x[1])
