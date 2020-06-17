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

def get_search_term(txt):

	r = re.search('([s|S][0-9][0-9][e|E][0-9][0-9])', txt)
	y = re.search('([(][1|2][0|9][0-9][0-9][)])', txt)
	# print(r.group())
	if y is not None:
	    # print(y.group())
	    txt = txt.replace(y.group(),'')
	ep = r.group()
	s = f'{ep[1]}{ep[2]}'
	if ep[1] == '0':
		s = f'{ep[2]}'

	e = f'{ep[4]}{ep[5]}'
	if ep[4] == '0':
		e = f'{ep[5]}'
	
	search_term = txt.split(ep)[0].strip()

	# print(search_term,s,e)
	return search_term,s,e

def list_format(c):
	count=0
	for i in c:
		i.insert(0, count)
		i[1] = textwrap.shorten(i[1], width=65, placeholder='..')
		count+=1
	return c
