import requests
from bs4 import BeautifulSoup

def zooqle_search(query):
	page = requests.get(f"https://zooqle.com/search?q={query}")
	soup = BeautifulSoup(page.content, 'lxml')
	# print(soup.prettify())

	b = []
	t_len = 60
	a = soup.find_all('a', class_=' small', href=True)
	#print(a)
	for x in a:
		c = []
		f = x.find_previous_sibling('i')
		#print(f)
		f=f['class']
		#print(f)
		
		if 'zqf-movies' in f or 'zqf-tv' in f:
			long_name = x.get_text()
			if '/' in long_name:
				long_name = long_name.split('/')[1].lstrip()
			filename = (long_name[:t_len] + '..') if len(long_name) > t_len else long_name
			c.append(f'[Zooqle] {filename}')
			magnet = x.find_next('a',title='Magnet link',href=True)
			c.append(magnet['href'])
			size = x.find_next('div', class_='progress-bar prog-blue prog-l')
			c.append(size.get_text())
			seedpeers = x.find_next('div',{'class': ['progress prog trans90', 'progress prog trans70']})
			if seedpeers == None:
				seedpeers = {'title':'No info'}
			seeds = seedpeers['title'].split('|')[0].lstrip('Seeders: ')
			peers = seedpeers['title'].split('|')[1].lstrip('Leechers: ')
			c.append(seeds)
			c.append(peers)
			b.append(c)
	return b

if __name__ == '__main__':
    print(zooqle_search('westworld s03e01'))