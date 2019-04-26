import sys
import re
import requests
from bs4 import BeautifulSoup


chapter = int(input("CHAPTER: ")) - 1


page = requests.get('https://azkabanaudiobook.com/deathly-hallows-jim-dale-book-7/#more-173')
html = page.content
soup = BeautifulSoup(html, 'html.parser')
data = []
links = []
regex = r"openload\.co/+.*?mime=true"
audio = []
download_links = []
for frame in soup.findAll("iframe"):
    data.append(list(frame.attrs.values()))

for x in range(len(data)):
    if not x % 2:
        links.append(data[x][2])

for link in links:
    page = requests.get(link)
    html = page.content
    soup = BeautifulSoup(html, 'html.parser')
    for y in soup.findAll('script'):
        for script in y:
            if "$(\"#jquery_jplayer_1\").jPlayer({" in script:
                audio.append(script)
                for code in audio:
                    download_links.append(re.findall(regex,code))





# # print(re.findall(regex,audio[0]))
# for link in links:
#     print(link)
print(download_links)
