import scrape

# The 1 here is the size of the result each query, the dates are rather self explanatory, and fore testing purposes, the user is defaulted to my last.fm username, vishwarrior, but you could change that by adding another string, being *your* last.fm username!
# sc = scrape.scrape("1", "2022-01-01", "TODAY", "YourLastfmUsernameHere")

sc = scrape.scrape("1", "2022-01-01", "TODAY")
print(sc.dailyScrobbles())
print(sc.dailyTracks())
