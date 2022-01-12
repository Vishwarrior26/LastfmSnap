import scrape
import csv

sc = scrape.scrape("100", "ALL")
print(sc.artistCounts())
