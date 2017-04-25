import requests
from lxml import etree
from bs4 import BeautifulSoup
import urllib
import json


json_url = "http://www.elle.com/ajax/slides/28967?template=listicle"
response = urllib.urlopen(json_url)
json_data = json.load(response)


url = 'http://best-books.publishersweekly.com/pw/best-books/2016/fiction'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'lxml')
data= soup.find_all("div", {"class":"rule-top"})
for item in data:
        print item.contents[1].text, item.contents[3].text.split('(',1)[0], 'Publisher Weekly'

