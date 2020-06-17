import opensubs
from titlovi import titlovi_search
from halo import Halo
from utils.my_tools import list_format, get_search_term

def search_subtitles(search_term,torrent_name):
	spinner = Halo(text=f'Searching for {search_term} subtitles', spinner='dots')
	spinner.start()

	a = [['No subtitle',None,None]]
	srch,s,e,g,movie = get_search_term(search_term,torrent_name)
	o = opensubs.opensub_search(search_term)
	if movie:
		t = titlovi_search(srch,g=g,movie=True)
	else:
		t = titlovi_search(srch,s=s,e=e)
	b = [['Custom Search',None,None]]

	c = a+o+t+b
	print(c)
	list_format(c)

	spinner.stop()

	return c

