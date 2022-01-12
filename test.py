import scrape

sc = scrape.scrape("100", "ALL", "", "cs188")
print(sc.scrobblesInfo())
sc = scrape.scrape("100", "ALL")
print(sc.scrobblesInfo())
