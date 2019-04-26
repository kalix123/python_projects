import sys
import re
import urllib.request
from bs4 import BeautifulSoup
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

chapter = int(input("CHAPTER: ")) - 1

class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        # print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()

page = Page('https://azkabanaudiobook.com/deathly-hallows-jim-dale-book-7/#more-173')
soup = BeautifulSoup(page.html, 'html.parser')
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
page = Page(links[chapter])
soup = BeautifulSoup(page.html, 'html.parser')
for y in soup.findAll('script'):
    for script in y:
        if "$(\"#jquery_jplayer_1\").jPlayer({" in script:
            audio.append(script)

for code in audio:
    download_links.append(re.findall(regex,code))



# # print(re.findall(regex,audio[0]))
# for link in links:
#     print(link)
print(download_links[0][0])
