import random
#datova struktura pro reprezentaci grafu je seznam sousedu
#z kazdeho vrcholu vede linearni spojovy seznam, ve kterem jsou jeho sousedi
class Node:
	def __init__(self, index, edge, next = None):
		self.next = next
		self.index = index
		self.edge = edge

def generate_graph(amount_of_nodes):
	g = []
	for i in range(amount_of_nodes):
		g.append(Node(i, 0))
		a = g[i]
	for i in range(amount_of_nodes):
		for j in range(amount_of_nodes):
			if i != j and random.randint(0,4) == 0:
				add_into_graph(g[i], g[j], random.randint(1, 50))
	return g

def menu(g):
	print('vrchol: Soused(delka hrany):')
	for i in range(number_of_nodes):
		a = g[i].next
		print('{0}: '.format('%5d'%i),end=' ')
		while a != None:
			print('{0}({1}) '.format('%2d'%a.index,'%2d'%a.edge), end='')
			a = a.next
		print()
	print('','Co mám udělat?','[1] Generovat nový graf','[2] Zneorientovat graf','[3] Vypsat konponenty souvislosti','[4] Najít nejkratší cestu','[5] Přidat vrchol','[6] Přidat hranu',sep='\n')

def make_DFS(v, nodes):
	global state
	print('%2d'%v,end=' ')
	state[v] = 1
	u = nodes[v]
	while u != None:
		if state[u.index] == 0:
			make_DFS(u.index,nodes)
		u = u.next

def find_components(nodes):
	global state
	print()
	print('komponenty po radcich:')
	for i in range(len(nodes)):
		if state[i] == 0:
			make_DFS(i, nodes)
			print()

def add_into_graph(v0,u,edge_weight,make_symetric = False):
	v = v0.next
	w = v0
	p = v0
	_make_symetric = make_symetric
	while v != None:
		if v.index == u.index:
			p.next = v.next
			_make_symetric = False
			v = p
		if v.edge < edge_weight or v.edge == edge_weight and v.index < u.index:
			w = v
		p = v
		v = v.next
	if _make_symetric == False:
		#if make_symetric: print('sys')
		w.next = Node(u.index, edge_weight, w.next)
	if not make_symetric:
		add_into_graph(u, v0, edge_weight, True)

def read_input(min, max, ch = '', again = False):
    if again:
        print('ZADEJTE ZNOVU{0}!'.format(' '+ch))
    _input = input()
    try:
        _input = int(_input)
        if _input > max or _input < min:
            read_input(min, max, ch, True)
        else:
            return _input
    except ValueError:
        read_input(min, max, ch, True)
		
def remove_directions(nodes):
	for v in nodes:
		u = v.next
		while u != None:
			add_into_graph(nodes[u.index], v, u.edge)
			u = u.next
	return nodes

def find_way(nodes, v0, vn):
	for v in nodes:
		v.edge = 99999
	v0.edge = 0
	beginning = Node(v0.index, v0.edge)
	P = {}
	while beginning != None and beginning.index != vn.index:
		v = nodes[beginning.index]
		w = v.next
		while w != None:
			print('\nv = {0}; w = {1}\nh({0}) = {2}; l({0}; {1}) = {3}; h({1}) = {4}'.format(v.index, w.index,v.edge, w.edge, nodes[w.index].edge))
			#_input()
			if v.edge + w.edge < nodes[w.index].edge:
				add_into_graph(beginning, Node(w.index, v.edge + w.edge), v.edge + w.edge)
				nodes[w.index].edge = v.edge + w.edge
				print('relaxuji:\nh({0}) = {2}; l({0}; {1}) = {3}; h({1}) = {4}'.format(v.index, w.index,v.edge, w.edge, nodes[w.index].edge))
				#_input()
				P[w.index] = v.index
			w = w.next
		beginning = beginning.next
	if beginning != None:
		print('\nNEJKRATSI CESTA Z {0} DO {1} MA DELKU {2} !!!'.format(v0.index,vn.index,vn.edge))
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

number_of_nodes = 10
state = []
g = generate_graph(number_of_nodes)
repeat = True
while repeat:
	state = [0 for i in range(number_of_nodes)]
	menu(g)
	choice = read_input(1, 8, 'cislo moznosti')
	state = [0 for i in range(number_of_nodes)]
	if choice == 1:
		print('Na kolika vrcholech?')
		number_of_nodes = read_input(0, 99)
		g = generate_graph(number_of_nodes)
	if choice == 2:
		g = remove_directions(g)
	if choice == 3:
		g = remove_directions(g)
		find_components(g)
	if choice == 5:
		number_of_nodes += 1
		g.append(Node(number_of_nodes-1, 0))
	if choice == 6:
		print('Z jakeho vrcholu?')
		v1 = read_input(0, number_of_nodes, 'vrchol v')
		print('Do jakeho?')
		v2 = read_input(0, number_of_nodes, 'vrchol w')
		while v1 == v2:
			v2 = read_input(0, number_of_nodes, 'vrchol w', True)
		print('Jak dlouhou?')
		d = read_input(1, 99999, 'delku')
		add_into_graph(g[v1], g[v2], d)
	if choice == 4:
		print('Z jakeho vrcholu?')
		v1 = read_input(0, number_of_nodes, 'vrchol v')
		print('Do jakeho?')
		v2 = read_input(0, number_of_nodes, 'vrchol w')
		find_way(g, g[v1], g[v2])
	print('\n','\n')
