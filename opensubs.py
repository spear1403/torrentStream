from pythonopensubtitles.opensubtitles import OpenSubtitles
import urllib.request
import gzip
import os

ost = OpenSubtitles() 
ost.login('spear1403', 'crnavrana')

def opensub_search(query, language='hrv'):

	data = ost.search_subtitles([{'sublanguageid':language, 'query':query}])
	#print(data)
	b = []
	for x in range(len(data)):
		title = data[x].get('SubFileName')
		b.append([title, data[x].get('SubDownloadsCnt'),
			'opensubtitles', data[x].get('SubDownloadLink')])
	return b

def opensubtitles_download(url,name):

	response = urllib.request.urlopen(url)
	with open(f'subtitles/{name}', 'wb') as outfile:
		outfile.write(gzip.decompress(response.read()))
	subtitle = f'subtitles/{name}'
	return subtitle
