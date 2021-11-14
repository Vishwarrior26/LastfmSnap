from bs4 import BeautifulSoup
import requests
url = "https://www.last.fm/user/vishwarrior/library/artists?from=2021-11-10&to=2021-11-10"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
#print(soup)
description = soup.find_all("meta", property="og:description")
temp = str(description[1])
print(type(temp))
init =temp.find('"')+1
fini = temp.find('"',init+1)
print(init)
print(fini)
print(temp[init:fini])
print(temp[init:fini].split(")"))
print(temp[init:fini].replace("(","").split(")"))

# print(temp)
# print(description[1])
# descriptionArray = []
# for temp in description:
#     print(temp)
#     descriptionArray.append(temp)
# print(type(description))
# print(description)
