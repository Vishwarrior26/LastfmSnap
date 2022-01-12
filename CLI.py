import scrape

print("Enter your last.fm username")
user = input()
print("Enter the date range you would like to get info about (YYYY-MM-DD) \nStart date:")
# print("Start date:")
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
    print("What would you like to get info about? (artists, albums, or tracks)")
    type = input().lower().strip()
    if type == "artists":
        print(sc.artistInfo())
        done = True
    elif type == "albums":
        print(sc.albumInfo())
        done = True
    elif type == "tracks":
        print(sc.trackInfo())
        done = True
    else:
        print("Couldn't parse input; try typing in lowercase without spaces")
