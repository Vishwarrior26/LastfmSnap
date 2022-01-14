import scrape

# sc = scrape.scrape("100", "ALL", "", "cs188")
# print(sc.scrobblesInfo())
sc = scrape.scrape("MAX", "ALL")
# print(sc.scrobblesInfo())

# sc = scrape.scrape("2", "2022-01-01", "TODAY")

# print(sc.trackInfo())
# print(sc.dailyArtists())
# print(sc.trackInfo())
# print(sc.dailyAlbums())
# print(sc.dailyTracks())
# for x in sc.dailyTracks():
#     print(x[1])

# print(sc.specArtist("Tool"))
# print(sc.specAlbum("Lateralus"))
# print(sc.specAlbumArtist("Tool"))
# print(sc.specTrack("Schism"))
print(sc.specTrackArtist("Ludwig Goransson"))
