import sys
import re
import requests
from bs4 import BeautifulSoup

def get_download_link(chapter):
    page = requests.get('https://azkabanaudiobook.com/stephen-fry-hp-sorcerers-stone-book-1/')
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
    if chapter == "all":
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
        return download_links
    else:
        page = requests.get(links[int(chapter)])
        html = page.content
        soup = BeautifulSoup(html, 'html.parser')
        for y in soup.findAll('script'):
            for script in y:
                if "$(\"#jquery_jplayer_1\").jPlayer({" in script:
                    audio.append(script)
                    for code in audio:
                        download_links.append(re.findall(regex,code))
        print(download_links[0])
        return "https://" + download_links[0][0]


#print(download_links)
