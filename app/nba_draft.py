import requests
import MySQLdb
from bs4 import BeautifulSoup
import re
part = '/year/2016'




def make_soup(url):
	r = requests.get(url)
	soupdata = BeautifulSoup(r.content, 'lxml')
	return soupdata

for x in range(1,3):
	soup = make_soup("http://insider.espn.go.com/nba/draft/rounds/_/round/" + str(x) + part)
	data = soup.find_all("tr", class_=re.compile("team"))

	try:
		for item in data:
			# c.execute("INSERT INTO nba_draft_2017 (`PK`, `FULL_NAME`, `FIRST_NAME`, `LAST_NAME`, `SCHOOL`, `POS`, `TEAMS`, `HGT`, `WT`) VALUES (%s,UPPER(%s),UPPER(%s),UPPER(%s),UPPER(%s),UPPER(%s),UPPER(%s),%s,%s)",
			# (item.contents[0].find_all("p", {"class":"overall-number"})[0].text, item.contents[2].text, item.contents[2].text.split(' ')[0], item.contents[2].text.split(' ')[1], item.contents[6].text, item.contents[5].text, item.contents[1].find_all("p", {"class":"team-name"})[0].text, item.contents[3].text, item.contents[4].text))
			print '\n', item.contents[0].find_all("p", {"class":"overall-number"})[0].text, item.contents[2].text.split(' ')[0], item.contents[2].text.split(' ')[1], item.contents[6].text, item.contents[5].text, item.contents[1].find_all("p", {"class":"team-name"})[0].text, item.contents[3].text, item.contents[4].text + ' lbs'
			# db.commit()
	except IndexError:
		pass
	else:
		'success'


