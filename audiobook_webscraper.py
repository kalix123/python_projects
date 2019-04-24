import requests
from bs4 import BeautifulSoup
import re

data = requests.get('https://azkabanaudiobook.com/deathly-hallows-jim-dale-book-7/#more-173')

soup = BeautifulSoup(data.text, 'html.parser')

data = []
links = []

for frame in soup.findAll("iframe"):
    data.append(list(frame.attrs.values()))

for x in range(len(data)):
    if not x % 2:
        links.append(data[x][2])

for link in links:
    data = requests.get(link)
    soup = BeautifulSoup(data.text, 'html.parser')
