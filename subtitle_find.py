import opensubs
from titlovi import titlovi_search
from halo import Halo
from utils.my_tools import list_format, get_search_term

def search_subtitles(search_term):
	spinner = Halo(text=f'Searching for {search_term}', spinner='dots')
	spinner.start()

	a = [['No subtitle',None,None]]
	o = opensubs.opensub_search(search_term)
	srch,s,e = get_search_term(search_term)
	t = titlovi_search(srch,s,e)
	b = [['Custom Search',None,None]]

	c = a+o+t+b

	list_format(c)

	spinner.stop()

	return c

