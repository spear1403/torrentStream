import os, sys, re
from lime import get_lime_magnet
from torrent_find import search_torrents
from subtitle_find import search_subtitles
from titlovi import titlovi_download
from opensubs import opensubtitles_download
from utils.my_tools import force_decode
from tabulate import tabulate


def play_torrent(torrent_link, sub=None):
	print("Starting...")
	if sub == None:
		command=f"webtorrent '{torrent_link}' -o 'torrent' --not-on-top --no-quit --mpv"
	else:
		command=f"webtorrent '{torrent_link}' -o 'torrent' --not-on-top --no-quit --mpv -t '{sub}'"
	# print(command)
	os.system(command)

def get_torrents(query):
	t = search_torrents(query)
	# my_table(title='Torrent search results',content=t)
	print(tabulate(t,headers=["Id", "Name", "Size", "Seeds", "Peers"],tablefmt='psql',
		colalign=('center','left','right','right','right')))
	return t

def get_subtitles(search_term):
	o = search_subtitles(search_term)
	print(tabulate(o,headers=["Id", "Name", "D.Count", "Source"],tablefmt='psql',
		colalign=('center','left','right','left')))
	return o

def download_subtitle(url,name,source='opensubtitles'):
	if os.path.exists('subtitles') == False:
		os.makedirs('subtitles')
	subtitle = None
	if source == 'titlovi':
		subtitle = titlovi_download(url)
	else:
		subtitle = opensubtitles_download(url,name)
	force_decode(subtitle)
	return subtitle

def main():
	movie = True
	query = input('Enter movie or TV show name: ')
	query = query.lower()
	if re.search('([s][0-9][0-9][e][0-9][0-9])', query) is not None:
		movie = False
	print(movie)
	t = get_torrents(query)
	torrent = int(input('Select the number of the torrent: '))
	while True:
		if torrent == 0:
			sys.exit()
		elif torrent == len(t)-1:
			query = input('Enter movie or TV show name: ')
			t = get_torrents(query)
			torrent = int(input('Select the number of the torrent: '))
		elif torrent > len(t):
			print('Incorrect number. Try again...')
			torrent = int(input('Select the number of the torrent: '))
		else:
			break

	torrent_link = t[torrent][5]
	if '[Lime]' in t[torrent][1]:
		torrent_link = get_lime_magnet(torrent_link)

	o = get_subtitles(query)
	sub = int(input('Select subtitles: '))
	while True:
		if sub == 0:
			subtitle = None
			break
		elif sub == len(o)-1:
			query = input('Subtitle search: ')
			o = get_subtitles(query)
			sub = int(input('Select subtitles: '))
		else:
			subtitle = download_subtitle(o[sub][4],o[sub][1],o[sub][3])
			break
			
	play_torrent(torrent_link, sub=subtitle)

if __name__ == '__main__':
	main()