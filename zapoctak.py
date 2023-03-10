import random
class soused:
	def __init__(self, index, hrana, next = None):
		self.next = next
		self.index = index
		self.hrana = hrana

def RandomGraph(pocet):
	v = []
	for i in range(pocet):
		v.append(soused(i, 0))
		a = v[i]
	for i in range(pocet):
		for j in range(pocet):
			if i != j and random.randint(0,4) == 0:
				pridej(v[i], v[j], random.randint(1, 50))
	return v

def menu(v):
	print('vrchol: soused(delka hrany):')
	for i in range(vrcholu):
		a = v[i].next
		print('{0}: '.format('%5d'%i),end=' ')
		while a != None:
			print('{0}({1}) '.format('%2d'%a.index,'%2d'%a.hrana), end='')
			a = a.next
		print()
	print('','Co mám udělat?','[1] Generovat nový graf','[2] Zneorientovat graf','[3] Vypsat konponenty souvislosti','[4] Najít nejkratší cestu','[5] Přidat vrchol','[6] Přidat hranu',sep='\n')

def DFS(v, seznam):
	global stav
	print('%2d'%v,end=' ')
	stav[v] = 1
	u = seznam[v]
	while u != None:
		if stav[u.index] == 0:
			DFS(u.index,seznam)
		u = u.next

def komponenty(seznam):
	global stav
	print()
	print('komponenty po radcich:')
	for i in range(len(seznam)):
		if stav[i] == 0:
			DFS(i, seznam)
			print()

def pridej(v0,u,cena,symetrizace = False):
	v = v0.next
	w = v0
	p = v0
	bool = symetrizace
	while v != None:
		if v.index == u.index:
			p.next = v.next
			bool = False
			v = p
		if v.hrana < cena or v.hrana == cena and v.index < u.index:
			w = v
		p = v
		v = v.next
	if bool == False:
		#if symetrizace: print('sys')
		w.next = soused(u.index, cena, w.next)
	if not symetrizace:
		pridej(u, v0, cena, True)

def ctecka(min, max, co = '', znovu = False):
	if znovu:
		print('ZADEJTE ZNOVU{0}!'.format(' '+co))
	vstup = input()
	try:
		vstup = int(vstup)
		if vstup > max or vstup < min:	
			ctecka(min, max, co, True)
		else:
			return vstup
	except ValueError:
		ctecka(min, max, co, True)
		
def zneorientuj(seznam):
	for v in seznam:
		u = v.next
		while u != None:
			pridej(seznam[u.index], v, u.hrana)
			u = u.next
	return seznam

def cesta(seznam, v0, vn):
	for v in seznam:
		v.hrana = 99999
	v0.hrana = 0
	zacatek = soused(v0.index, v0.hrana)
	P = {}
	while zacatek != None and zacatek.index != vn.index:
		v = seznam[zacatek.index]
		w = v.next
		while w != None:
			print('\nv = {0}; w = {1}\nh({0}) = {2}; l({0}; {1}) = {3}; h({1}) = {4}'.format(v.index, w.index,v.hrana, w.hrana, seznam[w.index].hrana))
			#input()
			if v.hrana + w.hrana < seznam[w.index].hrana:
				pridej(zacatek, soused(w.index, v.hrana + w.hrana), v.hrana + w.hrana)
				seznam[w.index].hrana = v.hrana + w.hrana
				print('relaxuji:\nh({0}) = {2}; l({0}; {1}) = {3}; h({1}) = {4}'.format(v.index, w.index,v.hrana, w.hrana, seznam[w.index].hrana))
				#input()
				P[w.index] = v.index
			w = w.next
		zacatek = zacatek.next
	if zacatek != None:
		print('\nNEJKRATSI CESTA Z {0} DO {1} MA DELKU {2} !!!'.format(v0.index,vn.index,vn.hrana))
	else:
		print('cesta z {0} do {1} neexistuje'.format(v0.index,vn.index))
	print('CESTA: ', end = '')
	x = vn.index
	p = []
	p.append(x)
	while x != v0.index:
		x = P[x]
		p.append(x)
	p.reverse()
	print(*p, sep = ', ')

vrcholu = 10
stav = []
v = RandomGraph(vrcholu)
navzdy = True
while navzdy:
	stav = [0 for i in range(vrcholu)]
	menu(v)
	volba = ctecka(1, 8, 'cislo moznosti')
	stav = [0 for i in range(vrcholu)]
	if volba == 1:
		print('Na kolika vrcholech?')
		vrcholu = ctecka(0, 99)
		v = RandomGraph(vrcholu)
	if volba == 2:
		v = zneorientuj(v)
	if volba == 3:
		v = zneorientuj(v)
		komponenty(v)
	if volba == 5:
		vrcholu += 1
		v.append(soused(vrcholu-1, 0))
	if volba == 6:
		print('Z jakeho vrcholu?')
		v1 = ctecka(0, vrcholu, 'vrchol v')
		print('Do jakeho?')
		v2 = ctecka(0, vrcholu, 'vrchol w')
		while v1 == v2:
			v2 = ctecka(0, vrcholu, 'vrchol w', True)
		print('Jak dlouhou?')
		d = ctecka(1, 99999, 'delku')
		pridej(v[v1], v[v2], d)
	if volba == 4:
		print('Z jakeho vrcholu?')
		v1 = ctecka(0, vrcholu, 'vrchol v')
		print('Do jakeho?')
		v2 = ctecka(0, vrcholu, 'vrchol w')
		cesta(v, v[v1], v[v2])
	print('\n','\n')