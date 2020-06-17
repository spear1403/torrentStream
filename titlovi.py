import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
import urllib.request
from io import BytesIO

def titlovi_search(query,s=None,e=None,g=None,movie=False):
	if g == None:
		g = ''
	query = query.replace(' ','+').lower()
	# print(query)
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
	if movie:
		url = f"https://titlovi.com/titlovi/?prijevod={query}&jezik=bosanski|hrvatski|srpski&t=1&{g}sort=6"
	else:
		url = f"https://titlovi.com/titlovi/?prijevod={query}&jezik=bosanski|hrvatski|srpski&t=2&s={s}&e={e}&{g}sort=6"
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.content, 'lxml')

	b = []
	if movie:
		a = soup.find_all('div', class_="moviePopup")
	else:
		a = soup.find_all('span', class_="s0xe0y")

	for x in a:
		t = x.find_previous_sibling('a').get_text()
		y = x.find_previous_sibling('i').get_text()
		z = x.find_parent('h3')
		g = z.find_next_sibling('h4').get_text().split('fps')[0]
		if g.count('/') > 2:
			groups = g.split('/')
			g = f"{'/'.join(groups[:3])}/\n   {'/'.join(groups[3:])}"
		title = f"{t} {x.get_text()} {y} \n   {g}"
		# print(title)
		d = z.find_next_sibling('div', class_='download')
		
		d_count = d.find('span').get_text()
		d_link = f"https://titlovi.com/download/?type=1&mediaid={z['data-id']}"
		b.append([title, d_count, 'titlovi', d_link])

	return b

def titlovi_download(url):
	response = urllib.request.urlopen(url)
	with ZipFile(BytesIO(response.read())) as zip: 
		b=[]
		z=None
		a=zip.namelist()
		print(a)
		if len(a)==1:
			zip.extractall(path=f'subtitles')
			return f'subtitles/{a[0]}'
		else:
			for x in a:
				info = zip.getinfo(x)
				if info.is_dir():
					z=x
					continue
				if x.endswith('.srt'):
					if z is not None:
						if z in x:
							continue
					b.append(x)
			if len(b)==1:
				zip.extract(b[0],path=f'subtitles')
				return f'subtitles/{b[0]}'
			else:
				print('There seems to be more than one subtitle in the archive.')
				for y in range(len(b)):
					print(f'  {y}. {b[y]}')
				c = int(input('Which one would you like? '))
				zip.extract(b[c-1],path=f'subtitles')
				return f'subtitles/{b[c-1]}'
