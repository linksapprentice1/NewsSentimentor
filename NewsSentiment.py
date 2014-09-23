from collections import namedtuple
from splinter import Browser
from pattern.en import sentiment
import BeautifulSoup
import threader
import urllib3
import re

Url = namedtuple('Url', 'start end')

class News:

   def __init__(self, url, regex):
      self.url = url
      self.sentiments = []
      self.regex = regex

   def getSentiments(self, term):
      return self._sentiments(self._articleLinks(term))

   def _articleLinks(self, term):
      with Browser('firefox') as browser:
         browser.visit(self._fullUrl(term))
         links = re.findall(self.regex, browser.html)
         return filter(lambda x: ".js" not in x, links)

   def _fullUrl(self, term):
      return self.url.start + term + self.url.end

   def _sentiments(self, links):
      threads = [threader.makeThread(self._sentiment, (link,)) for link in links]
      threader.joinThreads(threads)
      return self._returnAndClearSentiments()

   def _sentiment(self, link):
      s = sentiment(self._getPage(link))[0]
      self.sentiments.append(s)

   def _getPage(self, link):
      http = urllib3.PoolManager()
      headers= {"User-Agent" : 
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5"}
      return self._getText(http.request('GET', link, headers = headers).data)

   def _getText(self, data):
      soup = BeautifulSoup.BeautifulSoup(data)
      return ' '.join([''.join(node.findAll(text=True)) for node in soup.findAll('p')])

   def _returnAndClearSentiments(self):
      s = self.sentiments
      self.sentiments = []
      return s

class Fox (News):

   def __init__(self):
      fox_url = Url("http://www.foxnews.com/search-results/search?q=", 
                    "&submit=Search&ss=fn")
      regex = "(http:\/\/www.foxnews.com\/\w+\/\d+[^\">]+)\">"
      News.__init__(self, fox_url, regex)

class Cnn (News):

   def __init__(self):
      cnn_url = Url("http://www.cnn.com/search/?query=", 
                    "&x=0&y=0&primaryType=mixed&sortBy=relevance&intl=false")
      regex = "(http:\/\/www.cnn.com\/*\d+[^\">]+)\">"
      News.__init__(self, cnn_url, regex)
