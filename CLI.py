import scrape

print("Enter your last.fm username")
user = input()
print("Enter the date range you would like to get info about (YYYY-MM-DD) \nStart date:")
start = input()
print("End date (Date or TODAY):")
end = input()
print("How many entries would you like to get? (### or MAX)")
size = input()
sc = scrape.scrape(size, start, end, user)
# print("What would you like to get info about?\nPress 1 for Artists, 2 for Albums and 3 for Tracks")
# sc = scrape.scrape("100", "ALL")

done = False
while not done:
    print("What would you like to get info about? (artists, albums, tracks, artist counts, or scrobbles)")
    type = input().lower().strip()
    if type == "exit":
        done = True
    elif type == "artists":
        print(sc.artistInfo())
        # done = True
    elif type == "albums":
        print(sc.albumInfo())
        # done = True
    elif type == "tracks":
        print(sc.trackInfo())
        # done = True
    elif type == "artist counts" or type == "artistcounts":
        print(sc.artistCounts())
    elif type == "scrobbles":
        print(sc.scrobblesInfo())
    elif type == "setuser":
        user = input().strip()
        sc.setUser(user)
        print()
    elif type == "setsize":
        size = input()
        sc.setSize(size)
    elif type == "settime":
        print("Start date:")
        start = input()
        print("End date (Date or TODAY):")
        end = input()
        sc.setTime(start, end)
    # elif type == "export":
        # TODO Add function to export to CSV in scrape
    else:
        print("Couldn't parse input; try typing in lowercase without spaces")
