from bs4 import BeautifulSoup
import requests
url = "https://www.last.fm/user/vishwarrior/library/artists?from=2021-11-10&to=2021-11-10"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
#print(soup)
description = soup.find_all("meta", property="og:description")
print(description[1])
# descriptionArray = []
# for temp in description:
#     print(temp)
#     descriptionArray.append(temp)
# print(type(description))
# print(description)
