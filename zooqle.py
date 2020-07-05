import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

def zooqle_search(query):
	page = requests.get(f"https://zooqle.com/search?q={query}")
	soup = BeautifulSoup(page.content, 'lxml')
	# print(soup.prettify())
	# with open('page.txt', 'w') as f:
	# 	f.write(soup.prettify())

	b = []
	a = soup.find_all('i', {'class':['zqf zqf-tv text-muted2 zqf-small pad-r2','zqf zqf-movies text-muted2 zqf-small pad-r2']})
	# print(a)
	for x in a:
		title = x.find_next_sibling('a').get_text()
		if '/' in title:
			title = title.split('/')[1].strip()
		magnet = x.find_next('a',title='Magnet link',href=True)['href']
		# print(magnet)
		size = x.find_next('div', class_="progress-bar prog-blue prog-l")
		if size is not None:
			size = size.get_text()
		else:
			z = x.find_parent('td')
			size = z.find_next_sibling('td', {'class':'smaller'}).get_text()
		seedpeers = x.find_next('div',{'class': ['progress prog trans90', 'progress prog trans70']})
		if seedpeers == None:
			seedpeers = {'title':'No info'}
		seeds = seedpeers['title'].split('|')[0].lstrip('Seeders: ')
		peers = seedpeers['title'].split('|')[1].lstrip('Leechers: ')
		b.append([f'[Zooqle] {title}', size, seeds, peers,magnet])
	return b

if __name__ == '__main__':
    t = zooqle_search('carnival row s01e03')
    for i in t:
    	i.remove(i[4])
    print(tabulate(t,headers=["Name", "Size", "Seeds", "Peers"],tablefmt='grid'))