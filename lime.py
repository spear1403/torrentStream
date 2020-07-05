import requests
from bs4 import BeautifulSoup
import re

def lime_search(query):
	page = requests.get(f"https://wwv.límetorrents.cc/search/all/{query}/")
	soup = BeautifulSoup(page.content, 'lxml')

	b = []
	a = soup.find_all('a', class_='csprite_dl14')
	# print(a)
	for x in a:
		c = []
		chinese = False
		f = x.find_next_sibling('a')
		title = f.get_text()
		for q in title:
			if re.search(u'[\u4e00-\u9fff]', q) or re.search(u'([Ð¤Ð°Ð½Ñ])', q):
				chinese = True
				break
		if chinese:
			continue
		c.append(f'[Lime] {title}')
		d_link = f"https://wwv.límetorrents.cc{f['href']}"
		z = x.find_parent('td', class_='tdleft')
		size = z.find_next_siblings('td', class_='tdnormal')[1].get_text()
		if 'MB' in size:
			size = f'{size.split(".")[0]} MB'
		c.append(size)
		s = z.find_next_sibling('td', 'tdseed')
		p = z.find_next_sibling('td', 'tdleech')
		c.append(s.get_text())
		c.append(p.get_text())
		c.append(d_link)
		# print(c)
		b.append(c)
	# print(b)
	return b

def get_lime_magnet(url):
	page2 = requests.get(url)
	soup2 = BeautifulSoup(page2.content, 'lxml')
	m = soup2.find_all('a', class_="csprite_dltorrent")

	# Magnet download link
	magnet_link = m[2]['href']

	return magnet_link
