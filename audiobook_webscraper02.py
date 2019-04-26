import sys
import re
import requests
import time
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from bs4 import BeautifulSoup

class WebPage(QtWebEngineWidgets.QWebEnginePage):
    global download_links
    def __init__(self):
        super(WebPage, self).__init__()
        self.loadFinished.connect(self.handleLoadFinished)
    def start(self, urls):
        self._urls = iter(urls)
        self.fetchNext()

    def fetchNext(self):
        try:
            url = next(self._urls)
        except StopIteration:
            return False
        else:
            self.load(QtCore.QUrl(url))
        return True

    def processCurrentPage(self, html):
        time.sleep(1)
        url = self.url().toString()
        soup = BeautifulSoup(html, 'html.parser')
        for y in soup.findAll('script'):
            for script in y:
                if "$(\"#jquery_jplayer_1\").jPlayer({" in script:
                    audio.append(script)
                    download_links.append(re.findall(regex,script))
        print(len(download_links))

        # print('loaded: [%d chars] %s' % (len(html), url))
        if not self.fetchNext():
            QtWidgets.qApp.quit()

    def handleLoadFinished(self):
        self.toHtml(self.processCurrentPage)



page = requests.get('https://azkabanaudiobook.com/deathly-hallows-jim-dale-book-7/#more-173')
html = page.content
soup = BeautifulSoup(html, 'html.parser')
data = []
links = []
download_links = []
regex = r"openload\.co/+.*?mime=true"
audio = []
for frame in soup.findAll("iframe"):
    data.append(list(frame.attrs.values()))
for x in range(len(data)):
    if not x % 2:
        links.append(data[x][2])


app = QtWidgets.QApplication(sys.argv)
webpage = WebPage()
webpage.start(links)
sys.exit(app.exec_())
