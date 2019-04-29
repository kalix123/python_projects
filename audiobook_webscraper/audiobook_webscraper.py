import sys
import re
import requests
from bs4 import BeautifulSoup

#get download link/s given a chapter or "all"
#https://azkabanaudiobook.com/stephen-fry-hp-half-blood-prince-book-6/
def get_download_link(chapter, book_choice):
    book_choice = int(book_choice)
    book_list = open('book_links.txt', 'r').read().splitlines()
    #specify what page all the chapters are listed on
    page = requests.get(book_list[int(book_choice-1)])
    #remove the headers
    html = page.content
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    links = []
    regex = r"openload\.co/+.*?mime=true"
    audio = []
    download_links = ''
    #search page for iframes and append the values of the attributes
    for frame in soup.findAll("iframe"):
        data.append(list(frame.attrs.values()))
    #ittereate through the length of the data and if the value is odd then
    #append it to the list of links
    for x in range(len(data)):
        if not x % 2:
            links.append(data[x][2])
    #if the chapter is equal to all then retrieve all the links
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
    #else only retrieve the specifide chapter
    else:
        #request chapter number from list of links (subtract 1 because list starts at 0
        #and chapters start at 1)
        page = requests.get(links[int(chapter-1)])
        #remove headers (if this is not done errors arrise)
        html = page.content
        soup = BeautifulSoup(html, 'html.parser')
        #find all the scrpt tags on the page
        for script in soup.findAll('script'):
            #for all the characters in the script tag
            for chars in script:
                #check if that string is in the script
                if "$(\"#jquery_jplayer_1\").jPlayer({" in chars:
                    #if it is the append to the audio list
                    audio.append(script)
                    #itterate through the audio list
                    for code in audio:
                        search_object = str(code)
                        #use regex to find anythin that has openload.co/stream, and ends in ?mime=true
                        download_links = re.findall(regex,search_object)
        #print the download link for given chapter
        print(download_links[0])
        #return a link to it
        return "https://" + download_links[0]

#uncomment last two lines if you would like to use the webscraper seperate from the flask website
# chapter = int(input("What chapter? "))
# get_download_link(chapter, 6)
