import textwrap
import re
import os

def force_decode(fname):
	try:
		with open(fname, 'r', encoding='utf-8') as f:
			data = f.read()

	except UnicodeDecodeError:
		print("Couldn't decode with 'utf-8'")
		with open(fname, 'r', encoding='cp1250') as f:
			data = f.read()
		with open(fname + '.new', 'w',encoding="utf-8") as f:
			f.write(data)
		os.remove(fname)
		os.rename(f'{fname}.new',fname)

def get_search_term(txt,name):

	# print(txt,name)
	s = e = g = None
	movie = False
	r = re.search('([s|S][0-9][0-9][e|E][0-9][0-9])', txt)
	y = re.search('([1|2][0|9][0-9][0-9])', name)
	# print(r.group())
	# print(y.group())
	if r is not None:
		ep = r.group()
		s = f'{ep[1]}{ep[2]}'
		if ep[1] == '0':
			s = f'{ep[2]}'

		e = f'{ep[4]}{ep[5]}'
		if ep[4] == '0':
			e = f'{ep[5]}'
		search_term = txt.split(ep)[0].strip()
	else:
		if y is not None:
			g = f'g={y.group()}&'
		movie = True
		search_term = txt
	# print(search_term,s,e,g,movie)
	return search_term,s,e,g,movie

def list_format(c):
	count=0
	for i in c:
		i.insert(0, count)
		if len(i[1]) > 65:
			if not i[3] == 'titlovi':
				i[1] = f'{i[1][:62]}...'
		count+=1
	return c
