from zooqle import zooqle_search
from yts import yts_search
from lime import lime_search
from halo import Halo
from utils.my_tools import list_format


def search_torrents(query):
	spinner = Halo(text=f'Searching for {query}', spinner='dots')
	spinner.start()

	a = [['------Exit application------',None,None,None]]
	y = yts_search(query)
	z = zooqle_search(query)
	l = lime_search(query)
	b = [['--------Search Again--------',None,None,None]]

	t = a+y+z+l+b

	list_format(t)

	spinner.stop()

	return t