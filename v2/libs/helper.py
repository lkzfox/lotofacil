from itertools import combinations, permutations
import math
import functools
import re
import pprint


def maxSequencia(numeros):
	numeros.sort()
	maior = 0; atual = 0
	for n in range(len(numeros) - 1):
		if numeros[n] + 1 == numeros[n+1]:
			atual += 1
		else:
			if atual > maior:
				maior = atual
			atual = 0
	
	return max(maior + 1, atual + 1)

def qtdSequencias(numeros):
	numeros.sort()
	numeros = numeros.copy()
	numeros.append(0)
	quantidade = 0; eSeq = 0
	for n in range(len(numeros) - 1):
		if numeros[n] + 1 == numeros[n+1]:
			eSeq += 1
		else:
			if eSeq > 1: quantidade += 1
			eSeq = 0
	
	return quantidade

def maxDiferencaVizinhos(numeros):
	max = 0
	for n in range(1, len(numeros)):
		dif = numeros[n] - numeros[n-1]
		max = dif if dif > max else max
	
	return max

def quantidadeGrupo(numeros, maximo_grupo, maximo_possivel = 25):
	chave = []
	for n in range(1, math.ceil(maximo_possivel/maximo_grupo) + 1):
		chave.append(str(len([x for x in numeros if x > (n-1) * maximo_grupo and x <= n * maximo_grupo])))

	return '.'.join(chave)
	
def chaveNumeros(numeros):
	if len(numeros) == 0: return ''
	if len(numeros) == 1: return str(numeros[0]).rjust(2, '0')
	return functools.reduce(lambda c,p: str(c).rjust(2, '0') + str(p).rjust(2, '0'), numeros)

def numerosChave(chave):
	return [int(x) for x in re.split('(\d\d)', chave) if x != '']

def chaveImparParGrupo(numeros, tamanho):
	chave = []
	for n in range(math.ceil(len(numeros)/tamanho)):
		lista = numeros[n*tamanho:(n+1)*tamanho]
		chave.append(str(len([x for x in lista if x % 2 == 0 ])))
		chave.append(str(len([x for x in lista if x % 2 != 0 ])))

	return '.'.join(chave)

def chaveDiferencaRange(numeros, inicio, fim):
	chave = []
	for n in range(inicio, fim - 1):
		chave.append(str(numeros[n+1] - numeros[n]))

	return '.'.join(chave)

def chaveSomaPulando(numeros, pulo):
	chave = []
	for n in range(len(numeros) - pulo):
		chave.append(str(numeros[n] + numeros[n + pulo]))

	return '.'.join(chave)

def repeticoes(lista):
	comuns = list(range(1, 26))
	for n in lista:
		comuns = list(set(n['numeros']) & set(comuns))
		print(comuns)

	return comuns

def chavePosicoes(numeros, posicoes):
	lista = [numeros[ix] for (ix, p) in enumerate(numeros) if ix in posicoes]
	return chaveNumeros(lista)

def somaPosicoes(numeros, posicoes):
	lista = [numeros[ix] for (ix, p) in enumerate(numeros) if ix in posicoes]
	return sum(lista)

def multiplicarPosicoes(numeros, posicoes):
	total = 1
	for i in posicoes:
		total *= numeros[i]
	return total

def merge(*dicts):
	final_dict = {}
	for (idx, n) in enumerate(dicts):
		for k in n.keys():
			if (idx == 0):
				final_dict[k] = []
			
			final_dict[k].append(n[k])
	
	return final_dict

def intersecao(arr1: list, arr2: list, length = False):
	# print(arr1, arr2)
	lista = list(set(list(arr1)) & set(list(arr2)))
	return len(lista) if length else lista


def resolver(pos, ope, numeros):
	lista = []
	for p in pos:
		lista.append(numeros[p])
	resultado = lista[0]
	for idx, op in enumerate(ope):
		proximo = lista[idx+1]
		
		if op == '-': 
			resultado -= proximo
		elif op == '+': 
			resultado += proximo
		elif op == '*': 
			resultado *= proximo
		elif op == '/': 
			resultado /= proximo


	return resultado


def reduzir25(num : int) -> int:
	temp = num
	while temp > 25:
		temp -= 25

	return temp

def resolverSimples(ope, numeros):
	resultado = numeros[0]
	for idx, op in enumerate(ope):
		proximo = numeros[idx+1]
		
		if op == '-': 
			resultado -= proximo
		elif op == '+': 
			resultado += proximo
		elif op == '*': 
			resultado *= proximo
		elif op == '/': 
			resultado /= proximo


	return resultado

def resolverFuncao(posicoes = [0, 1], numeros = [5, 10], funcao = '7*P-3*P'):
	substituido = ''.join(re.findall(r'\d+|P|-|\+|\*|/', funcao))
	for p in posicoes:
		substituido = substituido.replace('P', str(numeros[p]), 1)

	operacoes = re.split(r'-|\+', substituido)

	mapa = {}
	for op in operacoes:
		numeros = [int(x) for x in re.findall(r'\d+', op)]
		operadores = re.findall(r'[^\d+]', op)

		mapa[op] = resolverSimples(operadores, numeros)
	
	for ori, nov in mapa.items():
		substituido = substituido.replace(ori, str(int(nov)))

	numeros = [int(x) for x in re.findall(r'\d+', substituido)]
	operadores = re.findall(r'-|\+', substituido)

	return resolverSimples(operadores, numeros)

def resolverPropriedades(prop, ope, dicionario):
	lista = [dicionario[p] for p in prop]
	resultado = lista[0]
	for idx, op in enumerate(ope):
		proximo = lista[idx+1]

		if op == '-': 
			resultado -= proximo
		elif op == '+': 
			resultado += proximo
		elif op == '*': 
			resultado *= proximo


	return resultado


def resolverRange(pos, ope, numeros, base, range):
	resultado = abs(resolver(pos, ope, numeros))
	return abs(base - resultado) <= range

def gerarChaves(row, retornando : bool = False):
	numeros = row['numeros']
	pares = [x for x in numeros if x % 2 == 0]
	chaves_possiveis = {
		'pares': str(len(pares)),
		'maior_sequencia': str(maxSequencia(numeros)),
		'quantidade_sequencias': str(qtdSequencias(numeros)),
		'diferenca_maxima': str(maxDiferencaVizinhos(numeros)),
		'soma_par': str(sum(pares)),
		'soma_0_10': str(somaPosicoes(numeros, range(11))),  
		'soma_1_11': str(somaPosicoes(numeros, range(2,12))), 
		'soma_2_12': str(somaPosicoes(numeros, range(3,13))),  
		'soma_3_13': str(somaPosicoes(numeros, range(4,14))), 
		'soma_4_14': str(somaPosicoes(numeros, range(5,15))),
		'quantidade_menores_10': str(len([x for x in numeros if x < 10])),
		'quantidade_entre_10_20': str(len([x for x in numeros if x >= 10 and x < 20])),
		'quantidade_maiores_20': str(len([x for x in numeros if x >= 20])),
		'quantidade_primos': str(len([x for x in numeros if x in [2,3,5,7,11,13,17,19,23]])),
		'quantidade_menores_13': str(len([x for x in numeros if x < 13])),
		'quantidade_maiores_13': str(len([x for x in numeros if x > 13])),
		'quantidade_meio': str(len(intersecao([7,8,9,12,13,14,17,18,19], numeros))),
		'quantidade_col_1': str(len(intersecao(list(range(1, 26, 5)), numeros))),
		'quantidade_col_2': str(len(intersecao(list(range(2, 26, 5)), numeros))),
		'quantidade_col_3': str(len(intersecao(list(range(3, 26, 5)), numeros))),
		'quantidade_col_4': str(len(intersecao(list(range(4, 26, 5)), numeros))),
		'quantidade_col_5': str(len(intersecao(list(range(5, 26, 5)), numeros))),
	}

	chaves_primeira_parte = list(chaves_possiveis.keys())

	chaves_segunda_parte = []
	combinacoes = list(combinations(range(0,15), 2)) + [[x] for x in range(0,15)]
	for com in combinacoes:
		# Usa soma das posições
		chave_2 = 'soma-' + '_'.join([str(x) for x in com])
		chaves_possiveis[chave_2] = str(somaPosicoes(numeros, com))
		chaves_segunda_parte.append(chave_2)
		# # Usa o valor das posições
		chave = '_'.join([str(x) for x in com])
		chaves_possiveis[chave] = chavePosicoes(numeros, com)
		chaves_segunda_parte.append(chave)


	# Combinando chaves de posição com as chaves principais
	chaves_combinadas = {}
	for p1 in chaves_primeira_parte:
		for p2 in chaves_segunda_parte:
			chave = '**'.join([p1,p2])
			valor = '.'.join([chaves_possiveis[p1], chaves_possiveis[p2]])
			chaves_combinadas[chave] = valor


	# Combinando todas as chaves entre si
	chaves_combinadas = {}
	for cc in combinations(chaves_possiveis.keys(),2):
		p1,p2=cc[0],cc[1]
		chave = '**'.join([p1,p2])
		valor = '.'.join([chaves_possiveis[p1], chaves_possiveis[p2]])
		chaves_combinadas[chave] = valor

	if retornando:
		return chaves_combinadas

	lista_chaves = []
	for c, v in chaves_combinadas.items():
		row[c] = v
		lista_chaves.append(c)

	return lista_chaves

def buscarQuantidadesSequencias(seq, lista, ocorrencias_crescente = False):
	sequencias = []
	sequencia_atual = 0
	for n in lista:
		if (intersecao(n.__dict__['numeros'], seq, True) == len(seq)):
			sequencia_atual += 1
			if ocorrencias_crescente: sequencias.append(sequencia_atual)
		else:
			if not ocorrencias_crescente and sequencia_atual > 0: sequencias.append(sequencia_atual)
			sequencia_atual = 0
			if ocorrencias_crescente: sequencias.append(sequencia_atual)

	if not ocorrencias_crescente and sequencia_atual > 0: 
		sequencias.append(sequencia_atual)
	elif ocorrencias_crescente:
		sequencias.append(sequencia_atual)

	return sequencias


def pegarPosicoes(lista, posicoes):
	return [lista[x] for x in posicoes]

def gerarEstruturaQuantitativa(lista):
	
	def _analiseSimples(funcao, valor):
		return {'funcao': funcao, 'valido': valor}
	
	estrutura = {
		'funcoes': [],
		'jogos': [],
	}
	for x in lista:
		analise_geral = {
			'concurso': x['concurso'],
			'analises': [
				_analiseSimples('Soma', not( x['soma'] > 225 or x['soma'] < 156)),
				_analiseSimples('Qtd Pares', not( x['pares'] < 5 or x['pares'] > 9)),
				_analiseSimples('Qtd Impares', not( x['impares'] < 6 or x['impares'] > 10)),
				_analiseSimples('Maior Sequência', not( x['maior_sequencia'] < 3 or x['maior_sequencia'] > 8)),
				_analiseSimples('Qtd Sequências', not( x['quantidade_sequencias'] < 1 or x['quantidade_sequencias'] > 4)),
				_analiseSimples('Qtd Nºs < 10', not( x['quantidade_menores_10'] < 3 or x['quantidade_menores_10'] > 8)),
				_analiseSimples('Qtd Nºs 10~20', not( x['quantidade_entre_10_20'] < 4 or x['quantidade_entre_10_20'] > 8)),
				_analiseSimples('Qtd Nºs > 20', not( x['quantidade_maiores_20'] < 1)),
				_analiseSimples('Qtd Nºs Primos', not( x['quantidade_primos'] < 3 or x['quantidade_primos'] > 8)),
				_analiseSimples('Diferença Máx.', not( x['diferenca_maxima'] > 7  or x['diferenca_maxima'] == 1)),
				_analiseSimples('Qtd Nºs < 13', not( x['quantidade_menores_13'] < 5 or x['quantidade_menores_13'] > 10)),
				_analiseSimples('Qtd Nºs > 13', not( x['quantidade_maiores_13'] < 4 or x['quantidade_maiores_13'] > 9)),
				_analiseSimples('Qtd Nºs Meio', not( x['quantidade_meio'] < 2 or x['quantidade_meio'] > 8)),
				_analiseSimples('Qtd Nºs Col 1', not( x['quantidade_col_1'] < 1)),
				_analiseSimples('Qtd Nºs Col 2', not( x['quantidade_col_2'] < 1)),
				_analiseSimples('Qtd Nºs Col 3', not( x['quantidade_col_3'] < 1)),
				_analiseSimples('Qtd Nºs Col 4', not( x['quantidade_col_4'] < 1)),
				_analiseSimples('Qtd Nºs Col 5', not( x['quantidade_col_5'] < 1)),
				_analiseSimples('Posição 0', not( x['numeros'][0] > 3)),
				_analiseSimples('Posição 1', not( x['numeros'][1] > 6)),
				_analiseSimples('Posição 2', not( x['numeros'][2] > 8)),
				_analiseSimples('Posição 3', not( x['numeros'][3] > 10)),
				_analiseSimples('Posição 4', not( x['numeros'][4] > 11)),
				_analiseSimples('Posição 5', not( x['numeros'][5] > 13)),
				_analiseSimples('Posição 6', not( x['numeros'][6] < 8 or x['numeros'][6] > 14)),
				_analiseSimples('Posição 7', not( x['numeros'][7] < 10 or x['numeros'][7] > 16)),
				_analiseSimples('Posição 8', not( x['numeros'][8] < 11 or x['numeros'][8] > 18)),
				_analiseSimples('Posição 9', not( x['numeros'][9] < 13 or x['numeros'][9] > 19)),
				_analiseSimples('Posição 10', not( x['numeros'][10] < 15 )),
				_analiseSimples('Posição 11', not( x['numeros'][11] < 17 )),
				_analiseSimples('Posição 12', not( x['numeros'][12] < 19 )),
				_analiseSimples('Posição 13', not( x['numeros'][13] < 20 )),
				_analiseSimples('Posição 14', not( x['numeros'][14] < 23 )),
			]
		}
		estrutura['jogos'].append(analise_geral)

	for analise in estrutura['jogos'][0]['analises']:
		estrutura['funcoes'].append(analise['funcao'])
		
		 
	

	return estrutura



def obterTodasSequencias(numeros, tamanho = 3):
	"""Obtém todas as sequencias de um certo tamanho em uma lista"""
	sequencias_encontradas = []
	for n in range(0, len(numeros) - tamanho + 1):
		sequencia = numeros[n + tamanho - 1] - numeros[n] == tamanho - 1
		if sequencia:
			sequencias_encontradas.append(numeros[n:n+tamanho])

	return sequencias_encontradas

# Gerar ranks de posições que tem pouca tendencia a acontecer
def ranquearOcorrencias(lista):
	rank = dict()
	for n in range(1,26):
		rank[str(n)] = 0
		
	aproximador = 0.0
	for jogo in lista:
		aproximador = round(aproximador + 0.00001, 5)
		numeros = jogo.numeros
		for num in numeros:
			str_num = str(num)
			rank[str_num] = round(rank[str_num] + 1 + aproximador, 5)
	
	ordenado = dict(sorted(rank.items(), key=lambda x: x[1])) 
	# pprint.pp(ordenado)
	return [int(x) for x in ordenado.keys()]

# Gerar ranks de acontecimentos
def ranquearListaNumeros(lista):
	'''Lista ordenada do rank de acontecimentos, sendo o mais recente o mais valioso'''
	rank = dict()
	for n in lista:
		rank[str(n)] = 0
		
	aproximador = 0.0
	for num in lista:
		aproximador = round(aproximador + 0.00001, 5)
		str_num = str(num)
		rank[str_num] = round(rank[str_num] + 1 + aproximador, 5)
	
	ordenado = dict(sorted(rank.items(), key=lambda x: x[1])) 
	# pprint.pp(ordenado)
	return [int(x) for x in ordenado.keys()]

## Descrição - Busca as chaves que apareceram em um certo jogo, e verificando a lista dos sorteios identifica quais numeros se repetiram para aquela combinação
# 1. Gera as combinações de uma certo sorteio
# 2. Busca as ocorrências das combinações que apareceram na lista de sorteios passadas
# 3. Retorna a lista dos números que apareceram para essas combinações
def buscarCombos(quantidade, numeros, jogos, numeros_saindo = True, visao_geral = False):
	combinacoes = list(combinations(numeros, quantidade))
	final = {}
	for comb in combinacoes:
		chave = '.'.join([str(x) for x in comb])
		final[chave] = {'ocorrencias': 0, 'numeros': list(range(26)), 'nunca': list(range(26))}
	for n in range(len(jogos)-1):
		numeros_jogo = jogos[n].numeros
		numeros_proximo_jogo = jogos[n+1].numeros
		for comb in combinacoes:
			chave = '.'.join([str(x) for x in comb])
			if len(intersecao(comb, numeros_jogo)) == len(comb):
				final[chave]['numeros'] = intersecao(final[chave]['numeros'], numeros_proximo_jogo)
				final[chave]['nunca']   = intersecao(final[chave]['nunca'], [x for x in range(1,26) if x not in numeros_proximo_jogo])
				final[chave]['ocorrencias'] = final[chave]['ocorrencias'] + 1
	
	unicos = set()
	if not visao_geral:
		final = dict(sorted(final.items(), key=lambda x: x[1]['ocorrencias'], reverse=True))
		for chave, valor in final.items():
			if len(valor['numeros']) < 3 and numeros_saindo: 
				# print(chave, valor)
				for n in valor['numeros']:
					unicos.add(n)

	else:
		final = dict(sorted(final.items(), key=lambda x: x[1]['ocorrencias'], reverse=False))
		for chave, valor in final.items():
			print(chave, valor)
	
	return list(unicos)

def mediaNumeros(numeros, div = None):
	if not div:
		div = len(numeros)
	return round(sum(numeros)/div)

def fatorarAnteriores(proximo, anteriores):
	montado = []
	for i, ant in enumerate(anteriores):
		posicoes = []
		comuns = intersecao(ant.numeros, proximo.numeros)
		for c in comuns:
			pos = ant.numeros.index(c)
			posicoes.append(pos)

		montado.append(posicoes)
	return montado

def numerosPares(numeros, posicoes = None):
	if not posicoes: posicoes = range(len(numeros))
	return [numeros[x] for x in posicoes if numeros[x] % 2 == 0]

def chaveImPa(numeros, posicoes):
	chave = ''
	for p in posicoes:
		chave += 'P' if numeros[p] % 2 == 0 else 'I'

	return chave

def buscarNumerosCaminho(lista, posicoes, caminho):
	caminho_valido = caminhoValido(caminho, len(lista) - 1)
	if not caminho_valido: return []
	linha_atual = 0
	numeros = []
	passos = list(caminho)
	for (c,p) in enumerate(posicoes):
		passo = passos[c]
		linha_atual += 1 if passo == 'D' else -1 if passo == 'S' else 0
		numeros.append(lista[linha_atual].numeros[p])

	return numeros


# Válido se está entre 0 e o máximo
def caminhoValido(caminho, maximo):
	inicio = 0
	niveis_usados = [inicio]
	for n in list(caminho):
		inicio += 1 if n == 'D' else -1 if n == 'S' else 0
		niveis_usados.append(inicio)
		if inicio < 0: return False
		if inicio > maximo: return False
	
	nivel_maximo = max(niveis_usados)
	return nivel_maximo == maximo


def chaveSequenciaPulo(numeros):
	chave = ''
	tamanho_sequencia = 0
	for n in range(len(numeros) - 1):
		diferenca = numeros[n+1] - numeros[n]
		if (numeros[n] + 1 == numeros[n+1]):
			tamanho_sequencia += 1
		elif tamanho_sequencia > 1:
			chave += 'S' + str(tamanho_sequencia+1) + 'P' + str(diferenca)
			tamanho_sequencia = 0
		else:
			tamanho_sequencia = 0
	
	if tamanho_sequencia > 0:
		chave += 'S' + str(tamanho_sequencia+1)

	return chave

def todasSequenciasPulos(numeros):
	chave = ''
	todas = []
	tamanho_sequencia = 0
	for n in range(len(numeros) - 1):
		diferenca = numeros[n+1] - numeros[n]
		if (numeros[n] + 1 == numeros[n+1]):
			tamanho_sequencia += 1
		elif tamanho_sequencia > 0:
			chave += 'S' + str(tamanho_sequencia+1) + 'P' + str(diferenca)
			tamanho_sequencia = 0
			todas.append(chave)
			chave = ''
		else:
			tamanho_sequencia = 0
	
	if tamanho_sequencia > 0:
		chave += 'S' + str(tamanho_sequencia+1)
		todas.append(chave)

	return todas

def quantidadeNumerosIrmaos(numeros):
	quantidade = 0
	for n in range(len(numeros) - 1):
		if (numeros[n] + 1 == numeros[n+1]):
			quantidade += 1

	return quantidade


def todasSequenciasPares(numeros, par = False):
	todas = []
	tamanho_sequencia = 0
	busca = 0 if par else 1
	for n in range(len(numeros) - 1):
		if (numeros[n] % 2 == busca and numeros[n] + 2 == numeros[n+1]):
			tamanho_sequencia += 1
		elif tamanho_sequencia > 0:
			seq = [numeros[x] for x in range(n, n - tamanho_sequencia - 1, -1)]
			seq.sort()
			todas.append(seq)
			tamanho_sequencia = 0
		else:
			tamanho_sequencia = 0

	return todas


def todasSquenciasTamanho(numeros, tamanho = 3):
	todas = []
	tamanho_sequencia = 0
	for n in range(len(numeros) - 1):
		if (numeros[n] + 1 == numeros[n+1]):
			tamanho_sequencia += 1
		elif tamanho_sequencia == tamanho - 1:
			seq = [numeros[x] for x in range(n, n - tamanho, -1)]
			seq.sort()
			todas.append(seq)
			tamanho_sequencia = 0
		else:
			tamanho_sequencia = 0
	
	return todas

def contemSquenciaCrescente(numeros, crescimento = [1,2,3,4]):
	for n in range(len(numeros) - len(crescimento)):
		valido = True
		numero_atual = numeros[n]
		for c in crescimento:
			temp = numero_atual + c
			valido = valido and temp in numeros

		if valido:
			return True
	
	return False

def analisarLista(lista):
	seguidos = True
	todos_seguidos = []
	qtd_seguidos = 0
	
	for n in range(len(lista)):
		ainda = lista[n] != 0
		if ainda:
			qtd_seguidos += 1
			seguidos = True
		else:
			if qtd_seguidos > 0:
				todos_seguidos.append(qtd_seguidos)
			seguidos = False
			qtd_seguidos = 0

	if qtd_seguidos > 0:
		todos_seguidos.append(qtd_seguidos)

	return {
		'max': max(todos_seguidos),
		'min': min(todos_seguidos)
	}

