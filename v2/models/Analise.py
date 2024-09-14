import pprint
import random
import pandas as pd
import time
import math
from itertools import combinations
from libs.helper import obterTodasSequencias, intersecao, somaPosicoes, chavePosicoes, maxDiferencaVizinhos, maxSequencia, chaveNumeros, resolver, pegarPosicoes, numerosChave, buscarCombos, ranquearOcorrencias, mediaNumeros, fatorarAnteriores, multiplicarPosicoes, numerosPares, resolverFuncao, chaveImPa, buscarNumerosCaminho, chaveSequenciaPulo, todasSequenciasPulos, quantidadeNumerosIrmaos, todasSequenciasPares, analisarLista, contemSquenciaCrescente, quantidadeGrupo, chaveDiferencaRange, chaveSomaPulando, reduzir25, ranquearListaNumeros
from libs.data_process import gerarSorteioSimples
from models.Sorteio import Sorteio

class alist(list):
	"""Classe auxiliar. Extesão da classe list"""
	def print(self, tamanho = False):
		for n in self:
			n.print()

		tamanho and print(len(self))

class Analise():
	sorteios: alist[Sorteio] = []
	combinacoes = {}
	ranks = {}
	
	def __init__(self, sorteios):
		for s in sorteios:
			self.setPendente(s)
		self.sorteios = alist(sorteios)

	def print(self):
		tamanho = len([x for x in self.sorteios if x.valido_analise != None])
		quantidade_valida = len([x for x in self.sorteios if x.valido_analise])
		acerto = round(quantidade_valida / tamanho, 2) if tamanho > 0 else 0

		pprint.pp({
			'Qtd Analisada': tamanho,
			'Qtd Válida': quantidade_valida,
			'Qtd Inválida': tamanho - quantidade_valida,
			'Acerto': acerto
		})

	def setInvalido(self, sorteio: Sorteio):
		sorteio.valido_analise = False
	def setValido(self, sorteio: Sorteio):
		if sorteio.valido_analise != False:  sorteio.valido_analise = True
	def setPendente(self, sorteio: Sorteio):
		sorteio.valido_analise = None
	def reset(self):
		for s in self.sorteios: 
			s.valido_analise = None
		return self

	## Descrição - Verificar sorteios que possuem sequencia igual ao sorteio anterior
	# 1. Gerar a lista de sequencias para os sorteios
	# 2. Verificar se o sorteio atual tem pelo menos uma sequência igual ao anterior
	# 3. Foi visto que para sequencias de 4 números, usando o intervalo de 40 e 49, quando analisado sobre os 100 últimos sorteios tem uma taxa de acerto de 90% e 83% para 1000 sorteios
	def sequenciaRepetidaJogoAnterior(self, intervalo = 1, tamanho_sequencia = 4):
		_sorteios = self.sorteios
		for sorteio in _sorteios:
			sorteio.setSequencias(tamanho_sequencia)
		
		qtd_com_repeticao, jogos_analisados = 0, 0
		for idx in range(intervalo, len(_sorteios)):
			anterior, proximo = _sorteios[idx - intervalo], _sorteios[idx]
			self.setValido(proximo)
			proximo.tem_sequencia_anterior = False
			jogos_analisados += 1
			if ValidacaoAnalise.sequenciaRepetidaJogoAnterior(proximo, anterior, tamanho_sequencia):
				proximo.tem_sequencia_anterior = True
				self.setInvalido(proximo)
				qtd_com_repeticao += 1

		acerto =  round(1 - qtd_com_repeticao / jogos_analisados, 2)
		qtd_com_repeticao < 230 and pprint.pp({
			'Intervalo': intervalo,
			'Jogos Analisados': jogos_analisados,
			'Qtd com repeticao': qtd_com_repeticao,
			'Acerto': acerto
		})
		
	## Descrição - Verificar se a soma de todas as posições pares, começando da 0 ocorre no sorteio anterior
	# 1. Gerar a soma das posições pares do sorteio
	# 2. Comparar com a soma das posições pares do sorteio seguinte
	def	compararSomaPosicoesPares(self):
		_sorteios = self.sorteios
		jogos_analisados = 0
		qtd_igual = 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx -1], _sorteios[idx]
			self.setValido(proximo)
			if ValidacaoAnalise.compararSomaPosicoesPares(proximo, anterior):
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		pprint.pp({
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		})

	## Descrição - Verificar se a soma de todas as posições impares, começando da 1 ocorre no sorteio anterior
	# 1. Gerar a soma das posições impares do sorteio
	# 2. Comparar com a soma das posições impares do sorteio seguinte
	def	compararSomaPosicoesImpares(self):
		_sorteios = self.sorteios
		jogos_analisados = 0
		qtd_igual = 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx -1], _sorteios[idx]
			self.setValido(proximo)
			if ValidacaoAnalise.compararSomaPosicoesImpares(proximo, anterior):
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		pprint.pp({
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		})

	## Descrição - Verificar se a ocorrencia em certas posições, ocorre com o mesmo número na mesma posição para o jogo anterior
	# 1. Verificar quais os números de uma posição
	# 2. Comparar a mesma posição do jogo anterior
	def	compararChavePosicoes(self, posicoes = [1,3,9,12], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados = 0
		qtd_igual = 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx -1], _sorteios[idx]
			self.setValido(proximo)
			if ValidacaoAnalise.compararChavePosicoes(proximo, anterior, posicoes):
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}

		not retornando and pprint.pp(retorno)
		return retorno
	

	## Descrição - Verificar se os valores de uma certa chave estão presentes em qualquer posição no jogo anterior
	# 1. Verificar quais os números de uma posição
	# 2. Comparar a os números do jogo anterior
	def	compararChavePosicoesComAnterior(self, posicoes = [1,3,9,12], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados = 0
		qtd_igual = 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx -1], _sorteios[idx]
			self.setValido(proximo)
			if ValidacaoAnalise.compararChavePosicoesComAnterior(proximo, anterior, posicoes):
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}

		not retornando and pprint.pp(retorno)
		return retorno
	
	## Descrição - Verificar se a soma do proximo jogo pode ser igual a soma do jogo anterior
	# 1. Comparar o valor de soma do proximo jogo com o jogo anterior
	def compararSomas(self):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx-1], _sorteios[idx]
			self.setValido(proximo)
			if ValidacaoAnalise.compararSomas(proximo, anterior):
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		pprint.pp(retorno)

	## Descrição - Verificar se certas caracteristicas podem ser iguais ao jogo anterior
	# 1. Para o proximo jogo verificar se as caracteristicas são iguais ao jogo anterior
	def compararCaracteristicas(self, caracteristicas = []):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx - 1], _sorteios[idx]
			self.setValido(proximo)

			if ValidacaoAnalise.compararCaracteristicas(proximo, anterior, caracteristicas):
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'Caracteristicas': caracteristicas
		}
		if qtd_igual == 1 or qtd_igual > 3000:
			f = open('./txt_temp/extras_10.txt', 'a')
			f.write(str(retorno))
			f.flush()
			pprint.pp(retorno)

	## Descrição - Verificar se a multiplicacao do proximo jogo pode ser igual a multiplicacao do jogo anterior
	# 1. Comparar o valor de multiplicacao do proximo jogo com o jogo anterior
	def compararMultiplicacoes(self):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx-1], _sorteios[idx]
			self.setValido(proximo)
			
			if ValidacaoAnalise.compararMultiplicacoes(proximo, anterior):
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		pprint.pp(retorno)

	## Descrição - Verificar se a soma de certas podições do proximo jogo pode ser igual a soma das mesmas posições do jogo anterior
	# 1. Comparar o valor de soma das posições do proximo jogo com a soma das mesmpas posições do jogo anterior
	def compararSomasMesmaPosicao(self, posicoes = [], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx-1], _sorteios[idx]
			self.setValido(proximo)
			soma1, soma2 = somaPosicoes(anterior.numeros, posicoes), somaPosicoes(proximo.numeros, posicoes)
			if soma1 == soma2:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if qtd_igual < 20:
			pprint.pp(posicoes)
			pprint.pp(retorno)
		
		if retornando: return retorno

	## Descrição - Buscar a quantidade de números que se repetem comparado com o jogo anterior
	# 1. Gerar um dicionário que tem chaves de 1 a 15
	# 2. Cada chave vai representar a quantidade de numeros repetidos entre o proximo jogo e o anterior
	def contarQuantidadeRepetida(self):
		_sorteios = self.sorteios
		jogos_analisados = 0

		quantidades = dict()
		for q in range(1, 16):
			quantidades[str(q)] = 0

		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx -1], _sorteios[idx]
			quantidade_comum = intersecao(proximo.numeros, anterior.numeros, True)
			quantidades[str(quantidade_comum)] += 1

		
		pprint.pp(quantidades)

	## Descrição - Buscar a quantidade de números que aparecem em uma certa posição
	# 1. Gerar um dicionário que tem chaves de 1 a 25
	# 2. Cada chave vai representar o número que apareceu, e seu valor é a quantidade de vezes
	def verificarPossibilidadePosicao(self, posicao = 0):
		_sorteios = self.sorteios
		quantidades = dict()
		for q in range(1, 26):
			quantidades[str(q)] = 0

		for sorteio in _sorteios:
			n = sorteio.numeros[posicao]
			quantidades[str(n)] += 1

		
		pprint.pp(quantidades)

	## Descrição - Buscar os valores máximos da diferença de números vizinhos
	# 1. Gerar um dicionário que tem chaves de 1 a 25
	# 2. Cada chave vai representar o número da diferença, e seu valor é a quantidade de vezes
	def verificarMaximaDiferencaVizinhos(self):
		_sorteios = self.sorteios
		quantidades = dict()
		for q in range(1, 26):
			quantidades[str(q)] = 0

		for sorteio in _sorteios:
			n = maxDiferencaVizinhos(sorteio.numeros)
			quantidades[str(n)] += 1

		
		pprint.pp(quantidades)

	## Descrição - Buscar os valores máximos da diferença de números vizinhos
	# 1. Gerar um dicionário que tem chaves de 1 a 25
	# 2. Cada chave vai representar o número da diferença, e seu valor é a quantidade de vezes
	def verificarTamanhoMaximoSequencia(self):
		_sorteios = self.sorteios
		quantidades = dict()
		for q in range(1, 26):
			quantidades[str(q)] = 0

		for sorteio in _sorteios:
			n = maxSequencia(sorteio.numeros)
			quantidades[str(n)] += 1

		
		pprint.pp(quantidades)

	## Descrição - Verificar se a soma dos primos do proximo jogo pode ser igual a soma dos primos do jogo anterior
	# 1. Comparar o valor da soma dos primos do proximo jogo com o jogo anterior
	def compararSomaPrimosIgual(self):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx-1], _sorteios[idx]
			self.setValido(proximo)
			
			if ValidacaoAnalise.compararSomaPrimosIgual(proximo, anterior):
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		pprint.pp(retorno)


	## Descrição - Buscar a quantidade de vezes que uma caracteristica aconteceu
	# 1. Gerar um dicionário que tem chaves com o valor da caracteristica
	# 2. Cada chave vai representar a caracteristica, e seu valor é a quantidade de vezes que essa aconteceu
	def verificarCaracteristica(self, caracteristica = ''):
		_sorteios = self.sorteios
		quantidades = dict()

		for sorteio in _sorteios:
			n = str(getattr(sorteio, caracteristica))
			if not quantidades.get(n):
				quantidades[n] = 0

			quantidades[n] += 1

		pprint.pp(dict(sorted(quantidades.items(), key=lambda x: x[0])))

	## Descrição - Verificar se a chave formada pela quantidade de numeros em um intervalo se repete
	# 1.Obter a chave formada pela quantidade de numeros de intervalo 5 (i.e. 1~5, 6~10...)
	# 2.Verificar se o jogo anteiror possuia a mesma chave
	def compararChavesIntervalos(self, intervalo = 5, distancia = 1):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(distancia, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx-distancia], _sorteios[idx]
			self.setValido(proximo)

			if ValidacaoAnalise.compararChavesIntervalos(proximo, anterior, intervalo):
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		pprint.pp(retorno)

	## Descrição - Verificar se a diferença entre certas posições acontecem no proximo sorteio
	# 1.Obter a cahve formada pela diferença de posições de um sorteio
	# 2.Verificar se o proximo jogo, aplicando a mesma regra, tem a chave repetida
	def compararDiferencaPosicaoSimples(self, passo = 1):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx-1], _sorteios[idx]
			self.setValido(proximo)
			
			if ValidacaoAnalise.compararDiferencaPosicaoSimples(proximo, anterior, passo):
				self.setInvalido(proximo)
				qtd_igual +=1
				# exit()

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		pprint.pp(retorno)

	## Descrição - Verificar se a soma de certas posições acontecem no proximo sorteio
	# 1.Obter a cahve formada pela soma de posições de um sorteio
	# 2.Verificar se o proximo jogo, aplicando a mesma regra, tem a chave repetida
	def compararSomaPosicaoSimples(self, passo = 1):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx-1], _sorteios[idx]
			self.setValido(proximo)
			
			if ValidacaoAnalise.compararSomaPosicaoSimples(proximo, anterior, passo):
				self.setInvalido(proximo)
				qtd_igual +=1
				# exit()

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		pprint.pp(retorno)

	## Descrição - Verificar se a soma de certas posições acontecem no proximo sorteio
	# 1.Obter a cahve formada pela soma de posições de um sorteio
	# 2.Verificar se o proximo jogo, aplicando a mesma regra, tem a chave repetida
	def compararOperacoesPosicoes(self, posicoes = [], operacoes = []):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx-1], _sorteios[idx]
			self.setValido(proximo)
			
			if ValidacaoAnalise.compararOperacoesPosicoes(proximo, anterior, posicoes, operacoes):
				self.setInvalido(proximo)
				qtd_igual +=1
				# exit()

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'Pos': posicoes,
			'Ope': operacoes,
		}
		pprint.pp(retorno)

	def compararOperacoesPosicoesV2(self, tamanho = 1, posicoes = [], operacoes = [], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		validos = []
		for idx in range(tamanho, len(_sorteios)):
			jogos_analisados += 1
			anteriores, proximo = _sorteios[idx-tamanho:idx], _sorteios[idx]
			self.setValido(proximo)

			valido = False
			for a in anteriores:
				resolvido = reduzir25(resolver(posicoes, operacoes, a.numeros))
				valido = valido or resolvido in proximo.numeros
				if valido:
					validos.append({'a': a.concurso, 'p': proximo.concurso, 'r': resolvido})
				# a.numeros.reverse()
				# resolvido = resolver(posicoes, operacoes, a.numeros)
				# valido = valido or resolvido in proximo.numeros
				# if valido:
				# 	validos.append({'a': a.concurso, 'p': proximo.concurso, 'r': resolvido})
			
			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'validos': validos[-tamanho:],
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.compararOperacoesPosicoesV2.__code__.co_varnames[1:self.compararOperacoesPosicoesV2.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Verificar se a combinação de algumas posições do sorteio n-2 e outras posições do n-1 acontecem no proximo
	# 1. Obter a lista dos numeros na posição do sorteio n-2
	# 2. Obter a lista dos números na posicao do sorteio n-1
	# 3. Verificar se o proximo jogo tem todos os números
	def compararCombinacaoSorteios(self, pos_sorteio1 = [], pos_sorteio2 = [], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(2, len(_sorteios)):
			jogos_analisados += 1
			aanterior, anterior, proximo = _sorteios[idx-2], _sorteios[idx-1], _sorteios[idx]
			self.setValido(proximo)

			if ValidacaoAnalise.compararCombinacaoSorteios(proximo, aanterior, anterior, pos_sorteio1, pos_sorteio2):
				self.setInvalido(proximo)
				qtd_igual +=1
				# exit()

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
		}
		if retornando: return retorno
		pprint.pp(retorno)


	## Descrição - Verificar se a combinação de algumas posições dos sorteios anteriores esão presentes no proximo sorteio
	# 1. Obter a lista dos numeros dos sorteios anteriores, de acordo com a quantidade de posições passadas, seguindo a ordem do mais antigo na primeira posição
	# 2. Verificar se o proximo jogo tem todos os números
	def compararCombinacaoSorteiosMultiplos(self, posicoes = [], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		tamanho = len(posicoes)
		for idx in range(tamanho, len(_sorteios)):
			jogos_analisados += 1
			proximo = _sorteios[idx]
			self.setValido(proximo)

			anteriores = _sorteios[idx-tamanho:idx]
			if ValidacaoAnalise.compararCombinacaoSorteiosMultiplos(proximo, anteriores, posicoes):
				self.setInvalido(proximo)
				qtd_igual +=1

				if qtd_igual > 66:
					break
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Verificar quantos sorteios uma chave formada por posições demora para se repetir
	# 1. Obter a lista dos numeros dos sorteios anteriores, de acordo com a posição passada
	# 2. Verificar quantos sorteios ocorrem sem a repetição da mesma chave
	def verificarRepeticaoChave(self, posicoes = [], retornando = False):
		_sorteios = self.sorteios
		repetido = False
		qtd_jogos_anteriores = 2
		for idx in range(qtd_jogos_anteriores, len(_sorteios)):
			repetido = ValidacaoAnalise.verificarRepeticaoChave(_sorteios[idx], _sorteios[idx-qtd_jogos_anteriores:idx], posicoes)
			if repetido: break

		pprint.pp({
			'Posicoes': posicoes,
			'Repetido': repetido
		})

		
	## Descrição - Verificar se certa caracteristica juntas com certas posições podem se repetir
	# 1. Para o proximo jogo verificar se as caracteristicas são iguais ao jogo anterior
	def compararCaracteristicaPosicao(self, caracteristica = 'primos', posicoes = [0,1,2,3,4], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx - 1], _sorteios[idx]
			self.setValido(proximo)

			if ValidacaoAnalise.compararCaracteristicaPosicao(proximo, anterior, caracteristica, posicoes):
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Verificar os acontecimentos de certos números, com os números do proximo sorteio, buscando quais grupos de números não aparecem no proximo
	# 1. Buscar todos os sorteios que acontecem os números e seu proximo
	# 2. Verificar no proximo sorteio as combinações que naõ acontecem
	# IDEIA - VERIFICAR OS NUMEROS QUE NAO SAIRAM NAS 6 PRIMEIRAS POSICOES, NESSA ORDEM
	def verificarNaoAcontecimentosPorNumeros(self, numeros = [0], tamanho = 1, posicoes = [0,1,2,3], retornando = False):
		combinacoes = combinations(numeros, tamanho)
		retorno = {}
		for comb in combinacoes:
			_sorteios = list(filter(lambda x : intersecao(x.numeros, comb, True) == len(comb), self.sorteios))
			# print(comb, len(_sorteios))
			idx_sorteios = 0
			inicio = time.time()
			for sorteio in self.sorteios:
				if idx_sorteios >= len(_sorteios): continue
				if (sorteio.concurso - 1) != _sorteios[idx_sorteios].concurso: continue
							
				
				chave = chavePosicoes(sorteio.numeros, posicoes)
				if not retorno.get(chave):
					retorno[chave] = 0

				retorno[chave] = retorno[chave] + 1
						
				idx_sorteios += 1
			
			# print(time.time() - inicio)


		lista_nao_sairam = []
		for c, va in retorno.items():
			if va not in range(1,7): continue
			# print(posicoes, numerosChave(c))
			# print(c, va)
			lista_nao_sairam.append((posicoes, numerosChave(c)))

		return lista_nao_sairam
		

	def _getCombinacoes(self, limite = (1,17), tamanho = 6):
		print('gerando', limite)
		for c in combinations(range(limite[0], limite[1]), tamanho):
			chave = chaveNumeros(c)
			self.combinacoes[chave] = 0
		
		return self.combinacoes
	

	def compararOcorrenciaRank(self, tamanho = 10, posicoes = [0]):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			jogos_analisados += 1
			anteriores, proximo = _sorteios[idx -tamanho:idx], _sorteios[idx]
			rank = self.aux_ranquearOcorrencias(anteriores)	
			if ValidacaoAnalise.compararOcorrenciaRank(proximo, anteriores, posicoes, rank):
				self.setInvalido(proximo)
				qtd_igual += 1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		return retorno

	
	# Gerar ranks de posições que tem pouca tendencia a contecer
	def aux_ranquearOcorrencias(self, lista):
		chave = str(lista[0].concurso) + '_' + str(lista[-1].concurso)
		if self.ranks.get(chave, False):
			return self.ranks[chave]
		
		rank = ranquearOcorrencias(lista)
		# pprint.pp(ordenado)
		self.ranks[chave] = rank
		return rank

	## Descrição Buscar as ocorreências recorrentes, no sorteio seguinte, das combinações de um sorteio
	# 1. Buscar as combinações de um sorteio, usando tamanho 2
	# 2. Verificar se os numeros que sempre apareceram, acontecem no proximo sorteio
	def compararOcorrenciasNumerosRecorrentes(self, tamanho = 0):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			jogos_analisados += 1
			anteriores, proximo = _sorteios[idx -tamanho:idx], _sorteios[idx]
			if ValidacaoAnalise.compararOcorrenciasNumerosRecorrentes(proximo, anteriores):
				self.setInvalido(proximo)
				qtd_igual += 1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		print(retorno)

	## Descrição - verificar a quantidade de vezes que uma série de números aparecem em sequencia
	# 1. Buscar os sorteios que apareceram os numeros
	# 2. Contar o maximo de vezes que essa série apareceu em sequencia
	def verificarQuantidadeRepeticoes(self, numeros = [], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual, contador, maximo = 0, 0, 0, 0
		descritivo = dict()
		for idx in range(len(_sorteios)):
			proximo = _sorteios[idx]
			if intersecao(proximo.numeros, numeros, True) != len(numeros): 
				contador = 0
				continue

			jogos_analisados += 1
			contador += 1
			maximo = max(contador, maximo)
			

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Máximo': maximo,
			'Contador Atual': contador,
			'valido': contador >= maximo
		}
		if retornando:
			return retorno
		print(retorno)

	## Descrição - Compara a chave gerada pela diferença das posicoes
	# 1. Gerar a chave da diferença das posicoes
	# 2. Verificar o proximo sorteio acontece a mesma chave
	def compararChaveOperacaoPosicoes(self, posicoes : list = [], operandos = ['-'], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx-1], _sorteios[idx]
			self.setValido(proximo)
			
			if ValidacaoAnalise.compararChaveOperacaoPosicoes(proximo, anterior, posicoes, operandos):
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if qtd_igual < 1:
			print(posicoes, operandos)
			pprint.pp(retorno)


	# Verificar se a estrutura do proximo sorteio fatorado tem a mesma chave entre as fatorações
	# 1. Buscar as fatorações do proximo sorteio
	# 2. Comparar com o sorteio anteiror na mesma posição da fatoração
	# 3. Base para a regra ValidacaoAnalise.compararFatoracaoIgual
	# IDEIA - Verificar se usando as top posições de cada sorteio dá pra acertar 11 com uma boa porcentagem
	def compararFatoracaoSorteiosAnteriores(self, qtd_iteracoes = 5, tamanaho_lista = 6, retornando = False, lista = None):
		if not lista:
			_sorteios = self.sorteios[-tamanaho_lista:]
		else:
			_sorteios = lista
		iteracoes = 0
		analitico, chave_ant = dict(), {}
		for n in range(qtd_iteracoes):
			analitico[str(n)] = {}
			chave_ant[str(n)] = []

		analitico['ger'] = {}
		for idx in range(qtd_iteracoes, len(_sorteios)):
			proximo = _sorteios[idx]
			anteriores = _sorteios[idx-qtd_iteracoes:idx]
			iteracoes += 1

			montado = []
			for i, ant in enumerate(anteriores):
				posicoes = []
				comuns = intersecao(ant.numeros, proximo.numeros)
				for c in comuns:
					pos = ant.numeros.index(c)
					posicoes.append(pos)

					conjunto_analitico = analitico[str(i)]
					if not conjunto_analitico.get(str(pos)):
						conjunto_analitico[str(pos)] = 0

					if not analitico['ger'].get(str(pos)):
						analitico['ger'][str(pos)] = 0

					conjunto_analitico[str(pos)] += 1
					analitico['ger'][str(pos)] += 1

				if chaveNumeros(chave_ant[str(i)]) == chaveNumeros(posicoes):
					if not retornando: print('---- TEM IGUAL ----', i)
				else:
					chave_ant[str(i)] = posicoes
				if not retornando: print(posicoes, i, pegarPosicoes(ant.numeros, posicoes))
				montado.append(posicoes)

		analitico['ger']['iteracoes'] = iteracoes
		analitico['ger']['iteracoes_maxima'] = iteracoes * qtd_iteracoes
		# print(_sorteios[0].concurso, _sorteios[-1].concurso)
		if retornando: return analitico
		pprint.pp(analitico)

	## Descrição - Verificar se em uma certa posição o numero é composto por uma combinaão de outros numeros do mesmo sorteio
	# 1. Buscar a posição específica
	# 2. Verificar se existe uma combinaçaõ de X dígitos que geram o numero na posição
	def verificarPosicaoESomaOutros(self, posicao = 9, qtd_soma = 2, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for sorteio in _sorteios:
			jogos_analisados += 1
			if not ValidacaoAnalise.verificarPosicaoESomaOutros(sorteio, posicao, qtd_soma):
				qtd_igual += 1

		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'Qtd Erros': jogos_analisados - qtd_igual
		}
		if retornando: 
			return retorno
		pprint.pp(retorno)

	## Descrição - Comparar se chave gerada pelas caracteristicas dos números do proximo sorteio ser igual a mesma chava do sorteio anterior
	# 1. Gerar a chave do sorteio seguinte
	# 2. Compara a chave do sorteio anterior com o proximo
	def verificarCaracteristicasPosicao(self, posicoes = [0], posicoes_chave = [], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx - 1], _sorteios[idx]
			self.setValido(proximo)
			
			if ValidacaoAnalise.verificarCaracteristicasPosicao(proximo, anterior, posicoes, posicoes_chave):
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Comparar se chave gerada pelas caracteristicas dos números do proximo sorteio pode ser igual a mesma chava do sorteio anterior
	# 1. Gerar a chave do sorteio seguinte
	# 2. Compara a chave do sorteio anterior com o proximo
	def verificarCaracteristicasPosicaoV2(self, posicoes = [0], posicoes_chave = [], modo = '', retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx - 1], _sorteios[idx]
			self.setValido(proximo)
			
			if ValidacaoAnalise.verificarCaracteristicasPosicaoV2(proximo, anterior, posicoes, posicoes_chave, modo):
				self.setInvalido(proximo)
				qtd_igual += 1

				if qtd_igual > 3: break
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		qtd_igual == 1 and pprint.pp(retorno)

	
	## Descrição - Verificar o intervalo alacançado ao aplicar uma função nas posições
	# 1. Gerar o valor da operação nos sorteios
	# 2. Usada para definir a função verificarFuncaoLista
	def verificarRangeOperacoes(self, posicoes = [], operacoes = []):
		_sorteios = self.sorteios
		encontrados = []
		for s in _sorteios:
			numero = resolver(posicoes, operacoes, s.numeros)
			encontrados.append(numero)

		encontrados = list(set(encontrados))
		print(posicoes, operacoes)
		print(max(encontrados), min(encontrados))
		print(encontrados)

	
	## Descrição - Verificar se gerando combinações de 13 números dos 17+ gerados apos analise da fatoração é possível ignorá-los no proximo sorteio
	# 1. Buscar os 17+ núemros gerandos pela fatoração ordenando crescentemente
	# 2. Verificar se o proximo sorteio tem pelo menos 13 dos números encontrados
	def verificarUsandoFuncao(self, tamanho = 2, quantidade_anteriores = 10, crescente = False, posicoes_ordenados = [0,1,2,3,4,5,6,7,8,9], tamanho_minimo = 16):
		_sorteios = self.sorteios
		quantidades, tam_intersecoes = [], []
		tamanho_lista = tamanho + quantidade_anteriores
		for idx in range(tamanho_lista, len(_sorteios)):
			resultado = self.compararFatoracaoSorteiosAnteriores(tamanho, 13, True, _sorteios[idx-tamanho_lista:idx])
			# pprint.pp(resultado)
			ultimos_sorteios, proximo = _sorteios[idx-tamanho:idx], _sorteios[idx]
			numeros_encontrados = []
			for pos_loop in posicoes_ordenados:
				if len(numeros_encontrados) >= tamanho_minimo: break
				for p in range(tamanho):
					ordenado = resultado[str(p)]
					ordenado = dict(sorted(ordenado.items(), key=lambda x: x[1], reverse = crescente))
					chaves_ordenadas = list(ordenado.keys())
					if pos_loop >= len(chaves_ordenadas): return ''
					chave = chaves_ordenadas[pos_loop]
					# print(chave)
					numeros_encontrados.append(ultimos_sorteios[p].numeros[int(chave)])

				numeros_encontrados = list(set(numeros_encontrados))

			# print(todos)
			# print(intersecao(todos, self.sorteios[-1].numeros, True))
			tam_intersecoes.append(len(numeros_encontrados))
			quantidades.append(intersecao(numeros_encontrados, proximo.numeros, True))

		maiores_13 = [x for x in quantidades if x > 13]
		print(len(maiores_13), maiores_13, mediaNumeros(tam_intersecoes))
		return (len(maiores_13), maiores_13, mediaNumeros(tam_intersecoes))
	
	def verificarUsandoFuncao_v2(self, tamanho = 2, quantidade_anteriores = 10, crescente = False, posicoes_ordenados = [0,1,2,3,4,5,6,7,8,9], tamanho_minimo = 16):
		_sorteios = self.sorteios
		quantidades, tam_intersecoes = [], []
		tamanho_lista = tamanho + quantidade_anteriores
		for idx in range(tamanho_lista, len(_sorteios)):
			resultado = self.compararFatoracaoSorteiosAnteriores(tamanho, 13, True, _sorteios[idx-tamanho_lista:idx])
			# pprint.pp(resultado)
			ultimos_sorteios, proximo = _sorteios[idx-tamanho:idx], _sorteios[idx]
			numeros_encontrados = []
			for pos_loop in posicoes_ordenados:
				if len(numeros_encontrados) >= tamanho_minimo: break
				for p in range(tamanho):
					ordenado = resultado[str(p)]
					ordenado = dict(sorted(ordenado.items(), key=lambda x: x[1], reverse = crescente))
					chaves_ordenadas = list(ordenado.keys())
					if pos_loop >= len(chaves_ordenadas): return ''
					chave = chaves_ordenadas[pos_loop]
					numeros_encontrados.append(ultimos_sorteios[p].numeros[int(chave)])

				numeros_encontrados = list(set(numeros_encontrados))

			# print(todos)
			# print(intersecao(todos, self.sorteios[-1].numeros, True))
			tam_intersecoes.append(len(numeros_encontrados))
			if intersecao(numeros_encontrados, proximo.numeros, True) < 11: return ''

		maiores_10 = [x for x in quantidades if x > 10]
		print(len(maiores_10), maiores_10, mediaNumeros(tam_intersecoes))
		return (len(maiores_10), maiores_10, mediaNumeros(tam_intersecoes))
	
	## Descrição - Verificar se utilizando a ordenação de certos sorteios, o numero com menos ocorrência está presente no sorteio atual e não presente no proximo
	# 1. Gerar o ranking dos ultimos sorteios
	# 2. Verificar se o sorteio atual contém o último número gerado e esse numero não está no proximo sorteio
	def verificarUsandoRanking(self, tamanho = 10, ultimos = 5, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		sequencia_erros = [0]
		for idx in range(tamanho, len(_sorteios)):
			jogos_analisados += 1
			resultado, proximo = ranquearOcorrencias(_sorteios[idx - tamanho:idx]), _sorteios[idx]
			
			numeros_ranqueados = resultado[-ultimos:]

			if intersecao(proximo.numeros, numeros_ranqueados, True) > 1:
			# if intersecao(proximo.numeros, numeros_ranqueados, True) == ultimos:
				qtd_igual += 1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarUsandoRanking.__code__.co_varnames[1:self.verificarUsandoRanking.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)
	
	## Descrição - Verificar qual o range de valores da soma de posições em uma quantidade de sorteios
	# 1. Buscar as posições dos sorteios
	# 2. Somar os valores das posições pela quanitdade de sorteios
	# 3. Obter a variancia daquelas posições
	# 4. Usada para definir a função de anáise verificarSomaPosicoesQuantidade
	def verificarSomaPosicoesQuantidade(self, posicoes = [0,1,2], quantidade_sorteios = 5):
		_sorteios = self.sorteios
		somas = []
		for idx in range(quantidade_sorteios, len(_sorteios)):
			agrupamento = _sorteios[idx-quantidade_sorteios:idx]
			numeros = []
			for sorteio in agrupamento:
				numeros.extend(pegarPosicoes(sorteio.numeros, posicoes))
			
			somas.append(sum(numeros))
		maximo, minimo = max(somas), min(somas)
		# print(maximo, minimo, maximo - minimo)
		return (maximo, minimo, maximo - minimo)

	## Descrição - Compara os sorteios que contem uma lista de números e seu multiplicador
	# 1. Buscar quantos sorteios contém os números selecionados e seu multiplicador
	def compararNumerosEMultiplicador(self, numeros = [1,2,3], multiplicador = 2):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for sorteio in _sorteios:
			jogos_analisados += 1
			self.setValido(sorteio)

			numeros_multiplicados = [x * multiplicador for x in numeros]
			condicao = intersecao(sorteio.numeros, numeros, True) == len(numeros) and intersecao(sorteio.numeros, numeros_multiplicados, True) == len(numeros)
			
			if condicao:
				self.setInvalido(sorteio)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if qtd_igual < 200:
			print(numeros)
			pprint.pp(retorno)
	
	## Descrição - Compara os sorteios que contem uma lista de números e seus multiplicadores
	# 1. Buscar quantos sorteios contém os números selecionados e seus multiplicadores
	def compararNumerosEMultiplicadorV2(self, numeros = [1,2,3], multiplicador = [2]):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for sorteio in _sorteios:
			jogos_analisados += 1
			self.setValido(sorteio)

			numeros_multiplicados = []
			for n in multiplicador:
				numeros_multiplicados.extend([x * n for x in numeros])

			numeros_multiplicados = list(set(numeros_multiplicados))
			condicao = intersecao(sorteio.numeros, numeros, True) == len(numeros) and intersecao(sorteio.numeros, numeros_multiplicados, True) == len(numeros_multiplicados)
			
			if condicao:
				self.setInvalido(sorteio)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if qtd_igual < 2:
			print(numeros)
			pprint.pp(retorno)

	
	## Descrição - Compara os sorteios que contem uma lista de números, suas somas ao 0 e suas subtrações ao 26
	# 1. Buscar quantos sorteios contém os números selecionados e seus multiplicadores
	def compararNumerosEConvergencia(self, numeros = [1,2,3], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for sorteio in _sorteios:
			jogos_analisados += 1
			self.setValido(sorteio)

			numeros_convergendo = list(numeros)
			numeros_convergendo.extend([x + 0 for x in numeros])
			numeros_convergendo.extend([26 - x  for x in numeros])

			numeros_convergendo = list(set(numeros_convergendo))
			condicao = intersecao(sorteio.numeros, numeros_convergendo, True) == len(numeros_convergendo)
			
			if condicao:
				self.setInvalido(sorteio)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		if qtd_igual == 1:
			print(numeros)
			pprint.pp(retorno)

	## Descrição - Comparar quantos sorteios possuem as subtrações entre as posições com mesmo valor entre elas
	# 1. calcular a operacao entre certas posicões
	# 2. verificar quantos sorteios possuem todas as diferenças iguais
	def verificarOperacaoPosicoes(self, posicoes = [[2,1]], operacao = '-', retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for sorteio in _sorteios:
			jogos_analisados += 1
			self.setValido(sorteio)
			
			if ValidacaoAnalise.verificarOperacaoPosicoes(sorteio, posicoes, operacao):
				self.setInvalido(sorteio)
				qtd_igual +=1
			
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Comparar quantos sorteios possuem as subtrações entre as posições com mesmo valor entre elas
	# 1. calcular a operacao entre certas posicões
	# 2. verificar quantos sorteios possuem todas as diferenças iguais
	def verificarContemOperacaoPosicoes(self, posicoes = [0,1], operacoes = ['-'], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for sorteio in _sorteios:
			jogos_analisados += 1
			self.setValido(sorteio)
			
			valor = resolver(posicoes, operacoes, sorteio.numeros)
			if valor in sorteio.numeros:
				self.setInvalido(sorteio)
				qtd_igual +=1
			
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Verificar quantos sorteios possuem as subtrações e as somas entre as posições no próprio sorteio
	# 1. calcular a subtração e a soma entre certas posicões
	# 2. verificar se o sorteio contém os dois valores resultantes
	def verificarContemSomaSubPosicoes(self, posicoes = [0,1], operacoes = [], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for sorteio in _sorteios:
			
			sub = resolver(posicoes, operacoes[0], sorteio.numeros)
			som = resolver(posicoes, operacoes[1], sorteio.numeros)

			if sub < 1 or som > 25: continue

			jogos_analisados += 1
			self.setValido(sorteio)

			if sub in sorteio.numeros and som in sorteio.numeros:
				self.setInvalido(sorteio)
				qtd_igual +=1
			
		acerto =  round(1 - qtd_igual / max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)


	## Descrição - Compara os sorteios que da certa operação, quando aplicado a certas posições tais numeros não aparecem no sorteio seguinte
	# 1. Relaizar a operação para todas as posições
	# 2. Verficar se todos os resultados estão no sorteio seguinte
	def compaparaOperacaoPosicoesSorteioSeguinte(self, operacoes = [['-','+']], posicoes = [[2,1,0]], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(len(_sorteios)-1):
			atual, proximo = _sorteios[idx], _sorteios[idx+1]

			resolvidos = list(set([resolver(p, operacoes[i], atual.numeros) for i, p in enumerate(posicoes)]))

			if len([x for x in resolvidos if x < 1 or x > 25]) > 0: continue

			jogos_analisados += 1
			self.setValido(proximo)
			
			condicao = ValidacaoAnalise.compaparaOperacaoPosicoesSorteioSeguinte(proximo, atual, operacoes, posicoes)
			
			if condicao:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Verificar quantos sorteios acontecem de uma operação sobre certas posições ser igual a outra posição
	# 1. Resolver a operação
	# 2. Verificar se o resultado é o valor da posição passada
	def verificarOperacaoPosicaoExata(self, posicoes = [], operacoes = [], posicao_buscada = 0, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for sorteio in _sorteios:
			jogos_analisados += 1
			self.setValido(sorteio)

			condicao = ValidacaoAnalise.verificarOperacaoPosicaoExata(sorteio, posicoes, operacoes, posicao_buscada)
			
			if condicao:
				self.setInvalido(sorteio)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Verificar quantos sorteios tem o mesmo valor quando aplicada a subtração entre certas posições
	# 1. Resolver a operação para cada par de posição
	# 2. Verificar se o resultado é um único numero distinto
	def verificarSubtracaoUnicoNumero(self, posicoes = [], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for sorteio in _sorteios:
			jogos_analisados += 1
			self.setValido(sorteio)

			condicao = ValidacaoAnalise.verificarSubtracaoUnicoNumero(sorteio, posicoes)
			
			if condicao:
				self.setInvalido(sorteio)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Verificar quantos sorteios tem o valor de uma função aplicada a certas posicoes
	# 1. Resolver a operação para cada conjunto de posicoes
	# 2. Verificar se o resultado está entre os números do sorteio
	def verificarFuncaoContemNumeroGerado(self, posicoes = [], funcao = '', retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for sorteio in _sorteios:
			resolvido = resolverFuncao(posicoes, sorteio.numeros, funcao)
			if resolvido > 25 or resolvido < 1: continue

			jogos_analisados += 1
			self.setValido(sorteio)
			
			condicao = resolvido in sorteio.numeros
			
			if condicao:
				self.setInvalido(sorteio)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'fn': funcao,
			'pos': posicoes
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Verificar os valores entre a diferença da soma de certas posicoes de dois sorteios, utilizar os valores que só ocorreram uma vez como improváveis
	# 1. GErar a diferença da soma das posições dos sorteios
	# 2. Adicionar essa diferença em um contador
	# 3. Monitorar o contador
	def verificarSomasPosicoesComProximo(self, posicoes = [0,3,5]):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		somas = {}
		for idx in range(1, len(_sorteios)):
			anterior, proximo = _sorteios[idx-1],_sorteios[idx]
			dif = somaPosicoes(proximo.numeros, posicoes) - somaPosicoes(anterior.numeros, posicoes)
			if not somas.get(str(dif)):
				somas[str(dif)] = 0

			somas[str(dif)] += 1

		for num, qtd in somas.items():
			retorno = {
				'posicoes': posicoes,
				'numero': num,
				'quantidade': qtd
			}
			if qtd < 2:
				pprint.pp(retorno)
		
		# pprint.pp(df)
				
	def verificarSorteiosCombinacoesNoRank(self, posicoes = [0,3,5], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(100, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-100:idx],_sorteios[idx]
			jogos_analisados += 1
			self.setValido(proximo)
			
			ranqueado = ranquearOcorrencias(anteriores)

			if ValidacaoAnalise.verificarSorteiosCombinacoesNoRank(proximo, ranqueado, posicoes):
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'Posicoes': posicoes
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Verificar se existe alguma combinação das 13 posições que se repete entre os jogos
	# 1. Buscar o jogo anterior e o proximo
	# 2. VErificar se todas as combinações de 13 posições de cada jogo gera chaves únicas
	def verificarCombinacoesEntreSorteios(self, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-1:idx],_sorteios[idx]
			jogos_analisados += 1
			self.setValido(proximo)

			combinacoes = []
			for c in combinations(range(15), 13):
				for anterior in anteriores:
					combinacoes.append(chavePosicoes(anterior.numeros, c))
				combinacoes.append(chavePosicoes(proximo.numeros, c))

			total_unicos = len(list(set(combinacoes)))
			
			if total_unicos != 105 * 2:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Comparar se os intervalos possuem a mesma caracteristica
	def verificarCaracteristicaSubSorteioSorteios(self, tamanho = 11, caracteristica = 'pares', retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(len(_sorteios)):
			proximo = _sorteios[idx]
			jogos_analisados += 1
			self.setValido(proximo)

			caracteristicas = []
			sorteios_menores = [gerarSorteioSimples(proximo.numeros[x:x+tamanho]) for x in range(16-tamanho)]
			for s in sorteios_menores:
				caracteristicas.append(getattr(s, caracteristica))

			total_unicos = len(list(set(caracteristicas)))
			
			if total_unicos == 1:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)

		
	## Descrição - Verifica quantos numeros estão em certos ranges do rank
	# 1. Gerar rank de sorteios
	# 2. Verificar quantos números deve coter cada range
	def verificarQuantidadeNoRank(self, tamanho_rank = 10, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		quantidades = {}
		for idx in range(tamanho_rank, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho_rank:idx],_sorteios[idx]
			jogos_analisados += 1
			self.setValido(proximo)
			
			ranqueado = ranquearOcorrencias(anteriores)[16:]

			qtd_comum = str(intersecao(ranqueado, proximo.numeros, True))

			if not quantidades.get(qtd_comum):
				quantidades[qtd_comum] = 0

			quantidades[qtd_comum] += 1


		pprint.pp(dict(sorted(quantidades.items(), key = lambda x : x[1])))
		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)

	# IDEIA - Verificar se a quantidade de números em certos intervalos é a mesma
		
	## Descrição - Verificar se para certa posição o número acontece junto com certas caracteristicas quando comparado ao sorteio anterior
	# 1. Buscar se os números de certas posições são os mesmos para o sorteio anterior e o atual
	# 2. Verificar também se outra caracteristica se repete entre as outras posições
	def verificarNumeroPosicaoCaracteristicas(self, posicoes = [0, 1], posicoes_caracteristica = [3,4], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		quantidades = {}
		for idx in range(1, len(_sorteios)):
			anterior, proximo = _sorteios[idx-1],_sorteios[idx]
			jogos_analisados += 1
			self.setValido(proximo)
			
			if ValidacaoAnalise.verificarNumeroPosicaoCaracteristicas(proximo, anterior, posicoes, posicoes_caracteristica):
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'Posicoes': posicoes,
			'Posicoes Carac': posicoes_caracteristica
		}
		if retornando: return retorno
		pprint.pp(retorno)

	## Descrição - Verificar se para certas posiçãos os números do sorteio anterior são os mesmos dos numeros que não sairam no proximo sorteio
	# 1. Buscar os números de certas posições do sorteio anterior são os mesmos dos numero que não sairam no sorteio seguinte
	def verificarNumeroPosicaoNumeroNao(self, posicoes = [0, 1], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			anterior, proximo = _sorteios[idx-1],_sorteios[idx]
			jogos_analisados += 1
			self.setValido(proximo)
			
			if ValidacaoAnalise.verificarNumeroPosicaoNumeroNao(proximo, anterior, posicoes):
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'Posicoes': posicoes
		}
		if retornando: return retorno
		pprint.pp(retorno)


	## Descrição - Verificar se o sorteio possui todos os números do número do concurso, levar em consideração os sorteios com concurso maior que 100 e com no mínimo 2 dígitos diferentes
	def verificarNumerosInversoAnterior(self, tamanho = 2, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx], _sorteios[idx]
			jogos_analisados += 1
			self.setValido(proximo)

			if ValidacaoAnalise.verificarNumerosInversoAnterior(proximo, anteriores):
				self.setInvalido(proximo)
				qtd_igual +=1
				# print(proximo.concurso, proximo.valido_analise)
				# print(diferentes, subs, ant_01, ant_02, qtd_igual)
				# return

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		if qtd_igual < 6:
			pprint.pp(retorno)

	## Descrição - Verificar se o sorteio possui todos os números do número do concurso, levar em consideração os sorteios com concurso maior que 100 e com no mínimo 2 dígitos diferentes
	def calcularMediaColunas(self, tamanho = 2, coluna = 0, sorteios = None, retornando = False):
		_sorteios = self.sorteios if not sorteios else sorteios
		somas = []	
		for idx in range(tamanho, len(_sorteios)):
			anteriores = _sorteios[idx-tamanho:idx]
			temp = []
			for a in anteriores:
				temp.append(a.numeros[coluna])

			soma = sum(temp)
			somas.append(soma)

		df = pd.DataFrame(data = somas)
		desc = df.describe(percentiles=[0.05,0.95]).to_dict()[0]
		retorno = {
			'media': mediaNumeros(somas),
			'minn': desc['5%'],
			'maxi': desc['95%'],
			'diff': desc['95%'] - desc['5%']
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def analisarCalcularMediaColunas(self):
		_sorteios = self.sorteios
		tamanho = 100
		final = []
		resposta = {}
		for idx in range(tamanho, len(_sorteios)):
			soma = []
			anteriores, proximo = _sorteios[:idx], _sorteios[idx]

			for n in range(15):
				ret = self.calcularMediaColunas(2, n, anteriores, True)
				soma.append(abs(ret['media'] - anteriores[-1].numeros[n]))

			# print(soma)
			comum = intersecao(proximo.numeros, soma, True)
			final.append(comum)

			if not resposta.get(str(comum)):
				resposta[str(comum)] = 0

			resposta[str(comum)] += 1

		resposta['resumo'] = {
			'media': mediaNumeros(final),
			'max': max(final),
			'min': min(final),
			'total': len(final)
		}
		# Análise executada, decidido ignorar 80 sorteios, ou seja, tem que ser entre 5 e 10
		# '12': 7,
		# '11': 56,
		# '10': 258,
		# '9': 635,
		# '8': 892,
		# '7': 727,
		# '6': 344,
		# '5': 97,
		# '4': 14,
		# '3': 2,
		# 'resumo': {'media': 8, 'max': 12, 'min': 3, 'total': 3032}}
		pprint.pp(resposta)
		
	## Descrição - Verificar qual é a soma das diferenças entre os número da esquerda e direita de certas posições
	# 1. Passar pelas posições, calcular a soma das diferenças
	def verificarSomaDiferencasEsqDir(self, posicoes = []):
		_sorteios = self.sorteios
		resposta = {}
		for sorteio in _sorteios:
			for n in posicoes:
				comum = sorteio.numeros[n] - sorteio.numeros[n-1] + sorteio.numeros[n+1] - sorteio.numeros[n]

				if not resposta.get(str(comum)):
					resposta[str(comum)] = 0

				resposta[str(comum)] += 1

		tamanho = len(resposta.keys())
		resposta['pos'] = posicoes
		if tamanho < 9:
			pprint.pp(resposta)

	def verificarSequenciaLinhas(self, posicoes = [1,2,3,4], caminho = 'PDDD', qtd_jogos = 2, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(qtd_jogos, len(_sorteios)):
			jogos_analisados += 1
			anteriores, proximo = _sorteios[idx-qtd_jogos:idx], _sorteios[idx]

			anteriores.append(proximo)
			encontrados = buscarNumerosCaminho(anteriores, posicoes, caminho)
			# encontrados.sort()
			
			sequencia_valida = True
			for i in range(len(encontrados) - 1):
				sequencia_valida = sequencia_valida and (encontrados[i] == (encontrados[i+1] - 1))

			if sequencia_valida:
				self.setInvalido(proximo)
				qtd_igual +=1

			if qtd_igual > 2:
				break

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'Posicoes': posicoes
		}

		if retornando: return retorno
		pprint.pp(retorno)

	def verificarSomaDifencaMaior1(self):
		_sorteios = self.sorteios
		resposta = {}
		final = []
		for idx in range(len(_sorteios)):
			soma = []
			proximo = _sorteios[idx]

			for n in range(1, 15):
				dif = proximo.numeros[n] - proximo.numeros[n-1]
				ret = dif if dif > 1 else 0
				soma.append(ret)

			# print(soma)
			comum = sum(soma)
			final.append(comum)

			if not resposta.get(str(comum)):
				resposta[str(comum)] = 0

			resposta[str(comum)] += 1

		resposta['resumo'] = {
			'media': mediaNumeros(final),
			'max': max(final),
			'min': min(final),
			'total': len(final)
		}

		pprint.pp(resposta)

	## Descrição - Verificar a distancia do número para o numero até a 7ª posição com o mínimo e da 8º posição pra frente com o máximo
	def verificarDistanciasNumeros(self):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for proximo in _sorteios:
			jogos_analisados += 1
			iguais = True
			for n in range(7):
				minimo = proximo.numeros[n] - 1
				maximo = 25 - proximo.numeros[14-n]
				iguais = iguais and minimo == maximo

			if iguais:
				self.setInvalido(proximo)
				qtd_igual +=1
				# print(proximo.concurso, proximo.valido_analise)
				# print(diferentes, subs, ant_01, ant_02, qtd_igual)
				# return

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		pprint.pp(retorno)

	## Descrição - Verificar a quantidade de vezes que um dígito aparece por sorteio
	def verificarQuantidadeDigitos(self):
		_sorteios = self.sorteios
		resposta = {}
		for idx in range(len(_sorteios)):
			esse = {}
			proximo = _sorteios[idx]
		
			for n in range(10):
				esse[str(n)] = 0
				if not resposta.get(str(n)):
					resposta[str(n)] = {'max': 0, 'min': 1000}
				
				for numero in proximo.numeros:
					if str(n) in list(str(numero)):
						esse[str(n)] += 1


			for (ch, vl) in esse.items():
				resposta[str(ch)]['max'] = max(resposta[str(ch)]['max'], vl)
				resposta[str(ch)]['min'] = min(resposta[str(ch)]['min'], vl)
					
		pprint.pp(resposta)

	## Descrição - Comparar se a chave gerada de acordo com a sequencia e pulo, de um sorteio pode ocorrer no proximo
	# 1. Gerar a chave de sequencia e pulo
	# 2. Comparar com a mesma chave do sorteio seguinte
	def	compararChaveSequenciaPulo(self):
		_sorteios = self.sorteios
		jogos_analisados = 0
		qtd_igual = 0
		for idx in range(len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx -1], _sorteios[idx]
			self.setValido(proximo)
			chave_anterior = chaveSequenciaPulo(anterior.numeros)
			chave_proximo = chaveSequenciaPulo(proximo.numeros)
			if chave_anterior == chave_proximo:
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		pprint.pp({
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		})

	def	verificarChavesPuloRepetido(self):
		_sorteios = self.sorteios
		jogos_analisados = 0
		qtd_igual = 0
		for idx in range(len(_sorteios)):
			jogos_analisados += 1
			proximo = _sorteios[idx]
			self.setValido(proximo)
			todas = todasSequenciasPulos(proximo.numeros)
			if len(todas) < 2:
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		pprint.pp({
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		})

	def	verificarQuantidadeIrmaos(self):
		_sorteios = self.sorteios
		jogos_analisados = 0
		qtd_igual = 0
		for idx in range(len(_sorteios)):
			jogos_analisados += 1
			proximo = _sorteios[idx]
			self.setValido(proximo)
			todas = quantidadeNumerosIrmaos(proximo.numeros)
			if todas < 6:
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		pprint.pp({
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		})

	def verificarSequenciaPar(self):
		_sorteios = self.sorteios
		jogos_analisados = 0
		qtd_igual = 0
		for idx in range(len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx -1], _sorteios[idx]
			self.setValido(proximo)
			if len(todasSequenciasPares(proximo.numeros, True)) > 3:
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		pprint.pp({
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		})


	def verificarNumerosNaoSairam(self):
		_sorteios = self.sorteios
		jogos_analisados = 0
		lista_nao = [[] for x in range(26)]
		for idx in range(len(_sorteios)):
			jogos_analisados += 1
			proximo = _sorteios[idx]
			
			for i in range(26):
				lista_nao[i].append(1 if i in proximo.numeros_nao else 0)
		
		resposta = {}
		for i in range(1,26):
			resposta[i] = analisarLista(lista_nao[i])

		return resposta

	def verificarNumeroxCaracteristica(self, numero = 1, caracteristica = ''):
		_sorteios = self.sorteios
		resposta = {}
		total = 0
		for idx in range(len(_sorteios)):
			proximo = _sorteios[idx]
			if numero not in proximo.numeros: continue

			total += 1
			soma =  getattr(proximo, caracteristica) 
			if not resposta.get(soma):
				resposta[soma] = 0
				
			resposta[soma] += 1

		resposta = dict(sorted(resposta.items(), key= lambda x : x[1]))

		# print(total)
		acc = 0
		lista = []
		for (qtd_carac, qtd_acont) in resposta.items():
			acc += qtd_acont
			porc = round(acc * 100/total, 2)
			# print(qtd_carac, porc)
			if porc > 6:
				lista.append(str(qtd_carac))

		lista = ', '.join(lista)
		# pprint.pp(resposta)

		print(f"'{caracteristica}': [{lista}],", end = ' ')

	def verificarSorteioComCrescimento(self, crescimento = [1,2,3,4]):
		_sorteios = self.sorteios
		jogos_analisados = 0
		qtd_igual = 0
		for idx in range(len(_sorteios)):
			jogos_analisados += 1
			proximo = _sorteios[idx]
			self.setValido(proximo)
			if contemSquenciaCrescente(proximo.numeros, crescimento):
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		return {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
	
	def verificarSomaUnicaPosicoes(self, posicoes = [0,1,2,3]):
		_sorteios = self.sorteios
		jogos_analisados = 0
		qtd_igual = 0
		for idx in range(len(_sorteios)):
			jogos_analisados += 1
			proximo = _sorteios[idx]
			self.setValido(proximo)
			todas_somas = []
			for i in range(len(posicoes)):
				pos = posicoes[i]
				pos_fim = posicoes[len(posicoes) - 1 -i]
				soma = proximo.numeros[pos] + proximo.numeros[pos_fim]
				todas_somas.append(soma)
			tamanho = len(list(set(todas_somas)))
			if tamanho == 1:
				self.setInvalido(proximo)
				qtd_igual += 1
		
		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		return {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}

	def verificarNumeroxCaracteristicaPosicoes(self, numero = 1, posicoes = [0], tipo = 'padrao'):
		_sorteios = self.sorteios
		resposta = {}
		total = 0
		for idx in range(len(_sorteios)):
			proximo = _sorteios[idx]
			if numero not in proximo.numeros: continue

			total += 1
			soma = ''
			if tipo == 'padrao':
				for posicao in posicoes:
					soma += 'P' if proximo.numeros[posicao] % 2 == 0 else 'I'
			elif tipo == 'extra':
				soma = str(proximo.quantidade_menores_6) + '.' + str(proximo.quantidade_menores_18)
			elif tipo == 'soma':
				soma = str(sum([proximo.soma_meio, proximo.quantidade_menores_18])) + '.' + str(sum([proximo.pares, proximo.soma_menores_13])) + '.' + str(sum([proximo.soma_entre_10_20, proximo.quantidade_maiores_20]))
			elif tipo == 'mods':
				soma += str(int((proximo.quantidade_menores_10) % somaPosicoes(proximo.numeros, posicoes))) + '.' + str(proximo.pares)
			elif tipo == 'mods2':
				soma += str(int(proximo.soma / somaPosicoes(proximo.numeros, posicoes))) + '.'
			else:
				for posicao in posicoes:
					soma += 'P' if proximo.numeros[posicao] % 2 == 0 else 'I'
				for n in [proximo.pares]:
					soma += str(n)
				

			if not resposta.get(soma):
				resposta[soma] = 0
				
			resposta[soma] += 1

		resposta = dict(sorted(resposta.items(), key= lambda x : x[1]))

		# print(total)
		acc = 0
		lista = []
		lista_qtd = []
		porcent = {}
		for (qtd_carac, qtd_acont) in resposta.items():
			acc += qtd_acont
			porc = round(acc * 100/total, 2)
			porcent.setdefault(qtd_carac, porc)
			lista.append(porc)
			lista_qtd.append(qtd_acont)

		return {'resposta': resposta, 'numero': numero, 'posicoes': posicoes, 'porcent': porcent, 'lista': lista, 'lista_qtd': lista_qtd}


	def verificarNumeroxCaracteristicaColuna(self, coluna = 0, tamanho = 3, tipo = 'padrao', mods = []):
		_sorteios = self.sorteios
		resposta = {}
		total = 0
		for idx in range(tamanho, len(_sorteios)):
			lista = _sorteios[idx-tamanho:idx]
			numeros = [s.numeros[coluna] for s in lista]
			total += 1
			if tipo == 'padrao':
				soma = ''
				xx = 1
				for num in numeros:
					xx *= num
					soma += 'P' if xx % 2 == 0 else 'I'
			elif tipo == 'mods':
				soma = ''
				for n in [3,7]:
					soma += str(sum(numeros) % n) + '.'
			elif tipo == 'mods2':
				soma = ''
				for n in [5,8,11]:
					soma += str(sum(numeros) % n) + '.'
			elif tipo == 'dinamico':
				soma = ''
				for n in mods:
					soma += str(sum(numeros) % n) + '.'

			if not resposta.get(soma):
				resposta[soma] = 0
				
			resposta[soma] += 1

		resposta = dict(sorted(resposta.items(), key= lambda x : x[1]))

		# print(total)
		acc = 0
		lista = []
		porcent = {}
		for (qtd_carac, qtd_acont) in resposta.items():
			acc += qtd_acont
			porc = round(acc * 100/total, 2)
			porcent.setdefault(qtd_carac, porc)
			lista.append(porc)

		return {'resposta': resposta, 'coluna': coluna, 'porcent': porcent, 'lista': lista}


	def verificarNumerosxSomas(self, posicoes = [0], tamanho = 3, tipo = 'padrao', mods = []):
		_sorteios = self.sorteios
		resposta = {}
		total = 0
		for idx in range(tamanho, len(_sorteios)):
			lista = _sorteios[idx-tamanho:idx]

			numeros = []
			numeros_nao = []
			for (i, s) in enumerate(lista):
				posi = posicoes[i]
				numeros.append(s.numeros[posi])
				if posi < 10:
					numeros_nao.append(s.numeros_nao[posi])
					
			total += 1
			
		
			soma = ''
			if tipo == 'diffs':
				for i in range(1, len(numeros)):
					soma += str(abs(numeros[i] - numeros[i-1]))

			if tipo == 't01':
				for i in range(1, len(numeros_nao)):
					soma += str(abs(numeros_nao[i] - numeros_nao[i-1]))
					
			if tipo == 't02':
				for i in range(1, len(numeros_nao)):
					soma += str(abs(numeros_nao[i] - numeros_nao[i-1]))
				for i in range(1, len(numeros)):
					soma += str(abs(numeros[i] - numeros[i-1]))

			if tipo == 't03':
				for s in lista:
					soma += str(s.quantidade_menores_6)
					
			if not resposta.get(soma):
				resposta[soma] = 0
				
			resposta[soma] += 1

		resposta = dict(sorted(resposta.items(), key= lambda x : x[1]))

		# print(total)
		acc = 0
		lista = []
		porcent = {}
		for (qtd_carac, qtd_acont) in resposta.items():
			acc += qtd_acont
			porc = round(acc * 100/total, 2)
			porcent.setdefault(qtd_carac, porc)
			lista.append(porc)

		return {'resposta': resposta, 'posicoes': posicoes, 'porcent': porcent, 'lista': lista}

	def verificarNumerosPosicoesAnteriores(self, posicoes = [0, 1], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		tamanho = len(posicoes)
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			

			numeros_anteriores = []
			for (i, s) in enumerate(anteriores):
				numeros_anteriores.append(s.numeros[posicoes[i]])

			if len(list(set(numeros_anteriores))) != len(posicoes): continue

			jogos_analisados += 1
			self.setValido(proximo)

			chave_anterior = chaveNumeros(numeros_anteriores)
			chave_proximo = chavePosicoes(proximo.numeros, posicoes)
			
			if chave_anterior == chave_proximo:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'Posicoes': posicoes
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarChavePossivel(self, numeros = [1], caracteristicas = ['pares', 'quantidade_menores_10']):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		chaves_possiveis = {}
		for idx in range(1, len(_sorteios)):
			anterior, proximo = _sorteios[idx-1], _sorteios[idx]
			if intersecao(proximo.numeros, numeros, True) != len(numeros): continue

			jogos_analisados += 1
			
			chave = []
			for c in caracteristicas:
				chave.append(str(getattr(proximo, c)))

			chave_str = '.'.join(chave)

			if not chaves_possiveis.get(chave_str):
				chaves_possiveis[chave_str] = 0

			chaves_possiveis[chave_str] += 1
			
		chaves_possiveis['jogos_analisados'] = jogos_analisados
		retorno = dict(sorted(chaves_possiveis.items(), key = lambda x : x[1]))
		return retorno

	def verificarUltimosTodosNumeros(self, tamanho = 2, intervalo = [0,2], qtd_buscada = 4, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			numeros_anteriores = []
			for s in anteriores:
				numeros_anteriores.extend(s.numeros[intervalo[0]:intervalo[1]])


			numeros_encontrados = list(set(numeros_anteriores))
			qtd_numeros = len(numeros_encontrados)
			tem_sequencia = len(obterTodasSequencias(numeros_encontrados, qtd_buscada)) != 0
			if qtd_numeros == qtd_buscada:
				print(qtd_numeros, list(set(numeros_anteriores)), anteriores[0].concurso)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def compararChaveQuantidadeDistintosIntervalo(self, tamanho = 2, intervalo = 2, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			chave_anterior = []
			chave_atual = []
			for i in range(15-intervalo):
				n_ant = []
				n_atu = []
				for (p, a) in enumerate(anteriores):
					n_ant.extend(a.numeros[i:i+intervalo])
					if p > 0:
						n_atu.extend(a.numeros[i:i+intervalo])
						n_atu.extend(proximo.numeros[i:i+intervalo])
				
				chave_anterior.append(str(len(list(set(n_ant)))))
				chave_atual.append(str(len(list(set(n_atu)))))

			chave_atual = '.'.join(chave_atual)
			chave_anterior = '.'.join(chave_anterior)

			if chave_anterior == chave_atual:
				print(chave_atual, chave_anterior, anteriores[0].concurso)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def compararChaveQuantidadeIguaisIntervalo(self, tamanho = 2, intervalo = 2, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			chave_anterior = []
			chave_atual = []
			for i in range(15-intervalo):
				n_ant = list(range(1,26))
				n_atu = list(range(1,26))
				for (p, a) in enumerate(anteriores):
					n_ant = intersecao(a.numeros[i:i+intervalo], n_ant)
					if p > 0:
						n_atu = intersecao(a.numeros[i:i+intervalo], n_atu)
						n_atu = intersecao(proximo.numeros[i:i+intervalo], n_atu)
				
				chave_anterior.append(str(len(n_ant)))
				chave_atual.append(str(len(n_atu)))
			
			chave_atual = '.'.join(chave_atual)
			chave_anterior = '.'.join(chave_anterior)

			if chave_anterior == chave_atual:
				# print(chave_atual, chave_anterior, anteriores[0].concurso)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def compararChaveSomaPosicoes(self, tamanho = 1, posicoes = [[0,1],[1,2]], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			chave_anterior = []
			chave_atual = []
			
			total = 0
			for (p, a) in enumerate(anteriores):
				total += somaPosicoes(a.numeros, posicoes[p])
			chave_anterior.append(str(total))
				
			chave_atual.append(str(somaPosicoes(proximo.numeros, posicoes[-1])))
						
			chave_atual = '.'.join(chave_atual)
			chave_anterior = '.'.join(chave_anterior)

			tem_comum = intersecao(pegarPosicoes(anteriores[0].numeros, posicoes[0]), pegarPosicoes(proximo.numeros, posicoes[1]), True) > 0

			if chave_anterior == chave_atual and tem_comum:
				# print(chave_atual, chave_anterior, anteriores[0].concurso)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
		}
		if retornando: return retorno
		pprint.pp(retorno)

	
	def verificarSomaPosicoesPresenteProximo(self, tamanho = 1, posicoes = [0,2], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			somas = []
			for s in anteriores:
				somas.append(somaPosicoes(s.numeros, posicoes))

			somas = list(set([(soma % 25) + 1 for soma in somas]))
			if intersecao(somas, proximo.numeros, True) == len(somas):
				# print(anteriores[0].concurso, soma)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarSomaPosicoesAlgumPresenteProximo(self, tamanho = 1, posicoes = [0,2], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			somas = []
			for s in anteriores:
				somas.append(somaPosicoes(s.numeros, posicoes))

			somas = list(set([(soma % 25) + 1 for soma in somas]))
			iguais = intersecao(somas, proximo.numeros, True)
			if iguais > 0:
				# print(anteriores[0].concurso, soma)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'iguais': iguais
		}
		if retornando: return retorno
		pprint.pp(retorno)

	
	def verificarAlgumaChaveAnteriores(self, tamanho = 1, caracteristicas = ['pares', 'quantidade_menores_10'], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx], _sorteios[idx]

			jogos_analisados += 1
			
			chaves = []
			chaves_proximo = []
			for c in caracteristicas:
				chaves_proximo.append('.'.join([c, str(getattr(proximo, c))]))
				for a in anteriores:
					chaves.append('.'.join([c, str(getattr(a, c))]))

			
			if intersecao(chaves_proximo, chaves, True) > 0:
				# print(anteriores[0].concurso, chaves, chave_proximo)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarNenhumaChaveAnteriores(self, tamanho = 1, caracteristicas = ['pares', 'quantidade_menores_10'], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx], _sorteios[idx]

			jogos_analisados += 1
			
			chaves = []
			chaves_proximo = []
			for c in caracteristicas:
				chaves_proximo.append('.'.join([c, str(getattr(proximo, c))]))
				for a in anteriores:
					chaves.append('.'.join([c, str(getattr(a, c))]))

			
			if intersecao(chaves_proximo, chaves, True) == len(caracteristicas):
				# print(anteriores[0].concurso, chaves, chave_proximo)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarContemTodasSomas(self, tamanho = 1, tamanho_somas = 2, quantidade_buscada = 0, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		tamanhos = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx], _sorteios[idx]

			jogos_analisados += 1
			
			somas = []
			for n in range(0, 16 - tamanho_somas, tamanho_somas):
				for a in anteriores:
					soma = (sum(a.numeros[n:n+tamanho_somas]) % 25) + 1
					somas.append(soma)

			somas = list(set(somas))
			tamanhos.append(len(somas))
			if intersecao(somas, proximo.numeros, True) == quantidade_buscada:
				# print(anteriores[0].concurso, chaves, chave_proximo)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'Ultimo': mediaNumeros(tamanhos)
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarContemAlgumaChave(self, tamanho = 1, posicoes = [0,1,2], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		tamanhos = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx], _sorteios[idx]

			jogos_analisados += 1
			
			chaves = []
			for a in anteriores:
				soma = sum(pegarPosicoes(a.numeros, posicoes))
				for sm in range(soma-5, soma+6):
					chaves.append(sm)

			chave_proximo = sum(pegarPosicoes(proximo.numeros, posicoes))
			
			if chave_proximo in chaves:
				# print(anteriores[0].concurso, chaves, chave_proximo)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarContemAlgumaChave.__code__.co_varnames[1:self.verificarContemAlgumaChave.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarContemTodosNumeros(self, posicoes = [0,1,2], buscado = 3, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		tamanho = len(posicoes)
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx], _sorteios[idx]

			jogos_analisados += 1
			
			numeros = []
			for (i,a) in enumerate(anteriores):
				numeros.append(a.numeros[posicoes[i]])
			
						
			if intersecao(proximo.numeros, numeros, True) == buscado:
				# print(anteriores[0].concurso, chaves, chave_proximo)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarContemTodosNumeros.__code__.co_varnames[1:self.verificarContemTodosNumeros.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarContemTodosNumerosFuncao(self, posicoes = [0,1,2], buscado = 3, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		tamanho = len(posicoes)
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx], _sorteios[idx]

			jogos_analisados += 1
			
			numeros = []
			resultado = []
			for (i,a) in enumerate(anteriores):
				numeros.append(a.numeros[posicoes[i]])
				resultado.append(sum(pegarPosicoes(a.numeros, posicoes)))

			#, sum(numeros), multiplicarPosicoes(numeros, range(tamanho))]
			resultado = list(set([(x % 25) + 1 for x in resultado]))
			
			# print(resultado, proximo.numeros)
			# exit()
						
			if intersecao(proximo.numeros, resultado, True) == buscado:
				# print(anteriores[0].concurso, chaves, chave_proximo)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarContemTodosNumerosFuncao.__code__.co_varnames[1:self.verificarContemTodosNumerosFuncao.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarChavesGrupos(self, tamanho = 3, inicio = 1, fim = 13, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx], _sorteios[idx]

			jogos_analisados += 1
			
			resultado = []
			for (i,a) in enumerate(anteriores):
				resultado.append(chaveDiferencaRange(a.numeros, inicio, fim))

			#, sum(numeros), multiplicarPosicoes(numeros, range(tamanho))]
			resultado = list(set(resultado))
			
			chave_proximo = chaveDiferencaRange(proximo.numeros, inicio, fim)

			# print(chave_proximo, resultado)
			# exit()
						
			if chave_proximo in resultado:
				# print(anteriores[0].concurso, chaves, chave_proximo)
				self.setInvalido(proximo)
				qtd_igual +=1
		
		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarChavesGrupos.__code__.co_varnames[1:self.verificarChavesGrupos.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarPosicoesAlgumPresenteMesmaProximo(self, posicoes = [0,2], buscado = 3, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		tamanho = len(posicoes)
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			contador = 0
			for s in anteriores:
				contador += 1 if intersecao(pegarPosicoes(s.numeros, posicoes), proximo.numeros, True) == buscado else 0

			if contador > 0:
				# print(anteriores[0].concurso, soma)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarPosicoesAlgumPresenteMesmaProximo.__code__.co_varnames[1:self.verificarPosicoesAlgumPresenteMesmaProximo.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarPosicoesPresenteSalto(self, posicoes = [0,2], tamanho = 2, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			valido = False
			for s in anteriores:
				if intersecao(pegarPosicoes(s.numeros, posicoes), proximo.numeros, True) == len(posicoes):
					valido = True

			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarPosicoesPresenteSalto.__code__.co_varnames[1:self.verificarPosicoesPresenteSalto.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)
		
	def verificarSomaColunasPresenteProximo(self, tamanho = 3, colunas = [2,3,4], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			possibilidades = [0 for x in colunas]
			for (p,coluna) in enumerate(colunas):
				for s in anteriores:
					possibilidades[p] += s.numeros[coluna]

			possibilidades = [
				(n % 25) + 1 for n in possibilidades
			]

			# print(possibilidades, possibilidades_proximo, True)
			# exit()
			geral = range(26)
			for s in anteriores[-2:]:
				geral = intersecao(geral, s.numeros)
			geral = intersecao(geral, proximo.numeros, True)

			if intersecao(possibilidades, proximo.numeros, True) > 0:# and intersecao(pegarPosicoes(anteriores[-1].numeros, colunas), pegarPosicoes(proximo.numeros, colunas), True) > 0:
				# print(anteriores[0].concurso, soma)
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarSomaColunasPresenteProximo.__code__.co_varnames[1:self.verificarSomaColunasPresenteProximo.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarUmPorSorteioAnteriorInvertida(self, colunas = [0,1,2,3], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		tamanho = len(colunas)
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			valido = True
			c2 = list(colunas)
			c2.reverse()
			for (p,coluna) in enumerate(c2):
				valido = valido and (proximo.numeros[coluna] in anteriores[p].numeros)

			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarUmPorSorteioAnteriorInvertida.__code__.co_varnames[1:self.verificarUmPorSorteioAnteriorInvertida.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarUmPorSorteioAnterior(self, colunas = [0,1,2,3], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		tamanho = len(colunas)
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			valido = True
			c2 = list(colunas)
			for (p,coluna) in enumerate(c2):
				valido = valido and (proximo.numeros[coluna] in anteriores[p].numeros)

			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarUmPorSorteioAnterior.__code__.co_varnames[1:self.verificarUmPorSorteioAnterior.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarUmPorSorteioAnteriorAmbas(self, colunas = [0,1,2,3], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		tamanho = len(colunas)
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			valido = True
			for (p,coluna) in enumerate(colunas):
				valido = valido and (proximo.numeros[coluna] in anteriores[p].numeros)

			c2 = list([*colunas])
			c2.reverse()
			for (p,coluna) in enumerate(c2):
				valido = valido and (proximo.numeros[coluna] in anteriores[p].numeros)

			if valido:# and anteriores[0].pares == proximo.pares:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarUmPorSorteioAnteriorAmbas.__code__.co_varnames[1:self.verificarUmPorSorteioAnteriorAmbas.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarSomaPosicoesNoAnterior(self, tamanho = 1, intervalo = 2, buscado = 2, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			numeros = []
			for i in range(0, 15 - intervalo):
				numeros.append((sum(proximo.numeros[i:i+intervalo]) % 25) + 1)
			
			numeros = list(set(numeros))

			quantidade = intersecao(numeros, proximo.numeros, True)
			comuns = proximo.numeros
			for s in anteriores:
				comuns = intersecao(comuns, s.numeros)

			quantidade_comuns = len(comuns)

			if quantidade == buscado and quantidade_comuns == buscado:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarSomaPosicoesNoAnterior.__code__.co_varnames[1:self.verificarSomaPosicoesNoAnterior.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarChaveIntersecaoSomas(self, tamanho = 2, intervalos = [[0,7],[8,15]], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			quantidades = []
			quantidades_proximo = []
			for [i,f] in intervalos:
				temp = list(range(25))
				temp_proximo = proximo.numeros[i:f]
				for a in anteriores:
					temp = intersecao(temp, a.numeros[i:f])
				
				for a in anteriores[1:]:
					temp_proximo = intersecao(temp_proximo, a.numeros[i:f])
				
				quantidades.append(len(temp))
				quantidades_proximo.append(len(temp_proximo))
			
			chave_ant = '.'.join([str(x) for x in quantidades])
			chave_prox = '.'.join([str(x) for x in quantidades_proximo])

			# print(quantidades, chave_ant)
			# print(quantidades_proximo, chave_prox)
			# exit()

			if chave_ant == chave_prox:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarChaveIntersecaoSomas.__code__.co_varnames[1:self.verificarChaveIntersecaoSomas.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarIntersecaoContemMinimo(self, tamanho = 1, intervalos = [[0,7],[8,15]], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			quantidades_proximo = []
			for [i,f] in intervalos:
				quantidades_proximo.append(intersecao(proximo.numeros[i:f], anteriores[0].numeros[i:f], True))
			
			todos_maior = [x for x in quantidades_proximo if x > 3]

			# print(anteriores[0].numeros, anteriores[0].concurso)
			# print(proximo.numeros, proximo.concurso)
			# print(quantidades_proximo, chave_prox, intervalos, proximo.concurso)
			# exit()

			if len(todos_maior) == len(quantidades_proximo):
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarIntersecaoContemMinimo.__code__.co_varnames[1:self.verificarIntersecaoContemMinimo.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarSomaNaoPresentesNoProximo(self, tamanho = 1, posicoes = [0,1], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			somas = []
			for a in anteriores:
				somas.append(sum(pegarPosicoes(a.numeros_nao, posicoes)) % 25 + 1)
			
			somas = list(set(somas))

			alguma_carac = True
			for c in ['pares', 'quantidade_menores_12']:
				alguma_carac = alguma_carac and getattr(proximo, c) == getattr(anteriores[-1], c)

			if intersecao(somas, proximo.numeros, True) == len(somas) and alguma_carac:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarSomaNaoPresentesNoProximo.__code__.co_varnames[1:self.verificarSomaNaoPresentesNoProximo.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarModuloDiferencaPresentesNoProximo(self, tamanho = 1, posicoes = [0,1], caracteristicas = ['pares'], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			diferencas = []
			for a in anteriores:
				diferencas.append(abs(sum(pegarPosicoes(a.numeros, posicoes)) - sum(pegarPosicoes(proximo.numeros, posicoes))) % 25 + 1)
			
			diferencas = list(set(diferencas))

			valido = 0
			for c in caracteristicas:
				for a in anteriores:
					valido += 1 if getattr(proximo, c) == getattr(a, c) else 0

			if intersecao(diferencas, proximo.numeros, True) == 0 and valido > 3:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarModuloDiferencaPresentesNoProximo.__code__.co_varnames[1:self.verificarModuloDiferencaPresentesNoProximo.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarCaracteristicasMinimasPresentesNoProximo(self, tamanho = 1, caracteristicas = ['pares'], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			alguma_carac = False
			for c in caracteristicas:
				for a in anteriores:
					alguma_carac = alguma_carac or getattr(proximo, c) == getattr(a, c)

			if alguma_carac:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarCaracteristicasMinimasPresentesNoProximo.__code__.co_varnames[1:self.verificarCaracteristicasMinimasPresentesNoProximo.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarProximoNosAnteriores(self, tamanho = 1, buscado = 15, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			novos = []
			for a in anteriores:
				novos.extend(a.numeros)

			if len([x for x in novos if x in proximo.numeros]) == buscado:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarProximoNosAnteriores.__code__.co_varnames[1:self.verificarProximoNosAnteriores.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarProximoQuantidadeNosAnteriores(self, tamanho = 1, buscado = 15, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			valido = False
			for a in anteriores:
				valido = valido or intersecao(a.numeros, proximo.numeros, True) == buscado

			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarProximoQuantidadeNosAnteriores.__code__.co_varnames[1:self.verificarProximoQuantidadeNosAnteriores.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarProximoCaracteristicaseNosAnteriores(self, tamanho = 1, caracteristicas = ['pares'], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			carac_proximo = []
			for c in caracteristicas:
				carac_proximo.append(str(getattr(proximo, c)))
			carac_proximo = '.'.join(carac_proximo)

			valido = False
			for a in anteriores:
				carac_atual = []
				for c in caracteristicas:
					carac_atual.append(str(getattr(a, c)))
					
				carac_atual = '.'.join(carac_atual)
				# print(carac_atual, carac_proximo, a.concurso, proximo.concurso)
				valido = valido or carac_atual == carac_proximo

			if valido:
				# print(carac_atual, carac_proximo, proximo.concurso)
				# exit()
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarProximoCaracteristicaseNosAnteriores.__code__.co_varnames[1:self.verificarProximoCaracteristicaseNosAnteriores.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def analiseChaveDiferencaProximo(self, tamanho = 2, posicoes = [0,1,2], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			ch_temp = []
			ch_temp_prox = []
			for p in posicoes:
				ch_temp.append(str(abs(anteriores[0].numeros[p] - anteriores[1].numeros[p])))
				ch_temp_prox.append(str(abs(anteriores[-1].numeros[p] - proximo.numeros[p])))
			ch_temp = '.'.join(ch_temp)
			ch_temp_prox = '.'.join(ch_temp_prox)

		
			if ch_temp == ch_temp_prox:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.analiseChaveDiferencaProximo.__code__.co_varnames[1:self.analiseChaveDiferencaProximo.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarDeslocamentoPosicoes(self, tamanho = 1, posicoes = [0,1], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			chave_anterior = chavePosicoes(anteriores[0].numeros, posicoes)
			chave_proximo = chavePosicoes(proximo.numeros, [x+1 for x in posicoes])
			
		
			if chave_anterior == chave_proximo:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarDeslocamentoPosicoes.__code__.co_varnames[1:self.verificarDeslocamentoPosicoes.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarRepeticaoChaveDiferenca(self, tamanho = 1, posicoes = [0, 1], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			chave_anterior = []
			chave_proximo = []

			for (p, n) in enumerate(posicoes):
				if p == len(posicoes) - 1: continue
				chave_anterior.append(anteriores[0].numeros[posicoes[p+1]] - anteriores[0].numeros[posicoes[p]])
				chave_proximo.append(proximo.numeros[posicoes[p+1]] - proximo.numeros[posicoes[p]])
			
			if chave_anterior == chave_proximo:
				# print(chave_anterior, chave_proximo)
				# exit()
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarRepeticaoChaveDiferenca.__code__.co_varnames[1:self.verificarRepeticaoChaveDiferenca.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)


	def verificarRepeticaoPorPosicao(self, tamanho = 1, posicoes = [0, 1], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			quantidade_repetida = 0
			
			for a in anteriores:
				quantidade_repetida += intersecao(pegarPosicoes(a.numeros, posicoes), pegarPosicoes(proximo.numeros, posicoes), True)
			
			if quantidade_repetida > 0:
				# print(chave_anterior, chave_proximo)
				# exit()
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarRepeticaoPorPosicao.__code__.co_varnames[1:self.verificarRepeticaoPorPosicao.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarRepeticaoPorPosicaoComQuantidade(self, tamanho = 1, posicoes = [0, 1], buscado = 1, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			quantidade_repetida = 0
			
			for a in anteriores:
				quantidade_repetida += intersecao(pegarPosicoes(a.numeros, posicoes), pegarPosicoes(proximo.numeros, posicoes), True)
			
			if quantidade_repetida == buscado:
				# print(chave_anterior, chave_proximo)
				# exit()
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarRepeticaoPorPosicaoComQuantidade.__code__.co_varnames[1:self.verificarRepeticaoPorPosicaoComQuantidade.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarRepeticaoPorPosicaoComQuantidadeDiferente(self, tamanho = 1, posicoes = [0, 1], buscado = 1, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			quantidade_repetida = 0
			
			for a in anteriores:
				quantidade_repetida += intersecao(pegarPosicoes(a.numeros, posicoes), pegarPosicoes(proximo.numeros, posicoes), True)
			
			if quantidade_repetida != buscado:
				# print(chave_anterior, chave_proximo)
				# exit()
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarRepeticaoPorPosicaoComQuantidadeDiferente.__code__.co_varnames[1:self.verificarRepeticaoPorPosicaoComQuantidadeDiferente.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	
	def verificarRepeticaoPorPosicaoAnterioresComQuantidadeDiferente(self, tamanho = 1, posicoes = [0, 1], buscado = 1, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			quantidade_repetida = 0
			
			for a in anteriores:
				quantidade_repetida += intersecao(pegarPosicoes(a.numeros, posicoes), proximo.numeros, True)
			
			if quantidade_repetida != buscado:
				# print(chave_anterior, chave_proximo)
				# exit()
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarRepeticaoPorPosicaoAnterioresComQuantidadeDiferente.__code__.co_varnames[1:self.verificarRepeticaoPorPosicaoAnterioresComQuantidadeDiferente.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	
	def verificarGapsPresentesSeguinte(self, tamanho = 1, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			valido = False
			entrou = False
			for i in range(1, 15):
				inicio = anteriores[0].numeros[i-1]
				fim = anteriores[0].numeros[i]
				if fim - inicio < 3: continue
				valido = valido or intersecao(proximo.numeros, list(range(inicio, fim+1)), True) > 0
				entrou = True
				# print(inicio, fim, anteriores[0].concurso)
				# exit()
			
			if not entrou:
				valido = True

			if valido:				
				# print(chave_anterior, chave_proximo)
				# exit()
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarGapsPresentesSeguinte.__code__.co_varnames[1:self.verificarGapsPresentesSeguinte.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarTodosGapsPresentesSeguinte(self, tamanho = 1, buscado = 2, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			numeros = []
			for a in anteriores:
				for i in range(1, 15):
					inicio = a.numeros[i-1]
					fim = a.numeros[i]
					if fim - inicio < 2: continue
					numeros.append(inicio)
					numeros.append(fim)
				# print(inicio, fim, anteriores[0].concurso)
				# exit()
			
			numeros = list(set(numeros))
			numeros_comuns = intersecao(proximo.numeros, numeros, True) 
			
			# print(numeros, anteriores[0].concurso)
			if buscado == numeros_comuns:
				# print(anteriores[0].concurso, numeros)
				# exit()
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarTodosGapsPresentesSeguinte.__code__.co_varnames[1:self.verificarTodosGapsPresentesSeguinte.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarSomaPresenteSeguinte(self, tamanho = 1, posicoes = [0,1,2], somas = [0,0,0], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		medias = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			numeros = []
			for a in anteriores:
				for (p,v) in enumerate(somas):
					numeros.append(a.numeros[posicoes[p]] + somas[p])
					# print(inicio, fim, anteriores[0].concurso)
					# exit()
			
			numeros = list(set(numeros))
			numeros_comuns = intersecao(proximo.numeros, numeros, True) 
			medias.append(len(numeros))
			# print(numeros, somas, posicoes,  anteriores[0].concurso)
			# exit(0)
			if len(numeros) == numeros_comuns:
				# print(anteriores[0].concurso, numeros)
				# exit()
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'media': mediaNumeros(medias),
			'exem': medias[15:25],
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarSomaPresenteSeguinte.__code__.co_varnames[1:self.verificarSomaPresenteSeguinte.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarSomaMinimaPresenteSeguinte(self, tamanho = 1, posicoes = [0,1,2], somas = [0,0,0], minimo = 3, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		medias = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			numeros = []
			for a in anteriores:
				for (p,v) in enumerate(somas):
					numeros.append(a.numeros[posicoes[p]] + somas[p])
					# print(inicio, fim, anteriores[0].concurso)
					# exit()
			
			numeros = list(set(numeros))
			numeros_comuns = intersecao(proximo.numeros, numeros, True) 
			medias.append(len(numeros))
			# print(numeros, somas, posicoes,  anteriores[0].concurso)
			# exit(0)
			if numeros_comuns >= minimo:
				# print(anteriores[0].concurso, numeros)
				# exit()
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'media': mediaNumeros(medias),
			'exem': medias[15:25],
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarSomaMinimaPresenteSeguinte.__code__.co_varnames[1:self.verificarSomaMinimaPresenteSeguinte.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	
	def verificarSomaSequencialNaoTemTodosSeguinte(self, tamanho = 1, somas = [0,0,0], minimo = 15, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		medias = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1

			numeros = []
			for a in anteriores:
				for i in range(0, 15 - len(somas), len(somas)):
					for (p, v) in enumerate(somas):
						numeros.append((abs(a.numeros[i + p] + v) % 25) + 1)
						# print(inicio, fim, anteriores[0].concurso)
						# exit()
			
			numeros = list(set(numeros))
			numeros_comuns = intersecao(proximo.numeros, numeros, True) 
			medias.append(len(numeros))
			# print(numeros, somas, anteriores[0].concurso, numeros_comuns)
			# exit(0)
			if numeros_comuns >= minimo:
				# print(anteriores[0].concurso, numeros)
				# exit()
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'media': mediaNumeros(medias),
			'exem': medias[-10:],
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarSomaSequencialNaoTemTodosSeguinte.__code__.co_varnames[1:self.verificarSomaSequencialNaoTemTodosSeguinte.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarMediaNumerosPosicao(self, tamanho = 1, posicoes = [0,1], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		medias = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1
				
			numeros = []
			for p in posicoes:
				temps = []
				for a in anteriores:
					temps.append(a.numeros[p])

				media = int(mediaNumeros(temps))
				numeros.append(media)

			numeros = list(set(numeros))

				
			valido = intersecao(proximo.numeros, numeros, True) == len(numeros)
			
			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarMediaNumerosPosicao.__code__.co_varnames[1:self.verificarMediaNumerosPosicao.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarMediaNumerosPosicaoMinimo(self, tamanho = 2, posicoes = [0,1], minimo = 2, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		medias = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1
				
			numeros = []
			for p in posicoes:
				temps = []
				for a in anteriores:
					temps.append(a.numeros[p])

				media = int(mediaNumeros(temps))
				numeros.append(media)

			numeros = list(set(numeros))

				
			valido = intersecao(proximo.numeros, numeros, True) >= minimo
			
			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarMediaNumerosPosicaoMinimo.__code__.co_varnames[1:self.verificarMediaNumerosPosicaoMinimo.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarSomasProximaPosicao(self, tamanho = 1, posicoes = [0,1,2,3,4,5,6,7,8,9,10,11], somas = [2,0,1,0,1,-2,-1,-3,-2,1,0,0], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1
				
			numeros = []
			for (i, p) in enumerate(posicoes):
				numeros.append((abs(anteriores[0].numeros[p] + somas[i]) % 25)+ 1)

			numeros = list(set(numeros))

				
			valido = intersecao(pegarPosicoes(proximo.numeros, [x+1 for x in posicoes]), numeros, True) == 1


			# VErsao anterior cod 998
			# numeros = []
			# for (i, p) in enumerate(posicoes):
			# 	numeros.append(anteriores[0].numeros[p] + somas[i])

			# numeros = list(set(numeros))

				
			# valido = intersecao(pegarPosicoes(proximo.numeros, [x+1 for x in posicoes]), numeros, True) == len(numeros)
			
			
			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarSomasProximaPosicao.__code__.co_varnames[1:self.verificarSomasProximaPosicao.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarMediaDiferentesNoProximo(self, tamanho = 2, posicoes = [1], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		resultados = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1
				
			numeros = []
			for (i, p) in enumerate(posicoes):
				temp = []
				for a in anteriores:
					temp.append(a.numeros[p])

				numeros.append(mediaNumeros(temp))
			
			numeros = list(set(numeros))

			resultados.append(intersecao(proximo.numeros, numeros, True))	
			valido = intersecao(proximo.numeros, numeros, True) > 0

			
			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'resultados': resultados[-10:],
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarMediaDiferentesNoProximo.__code__.co_varnames[1:self.verificarMediaDiferentesNoProximo.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	
	def verificarMediaDiferentesNoProximoV2(self, tamanho = 2, posicoes = [1], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		resultados = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1
				
			numeros = []
			for (i, p) in enumerate(posicoes):
				temp = []
				for a in anteriores:
					temp.append(a.numeros[p])

				temp = list(set(temp))
				numeros.append(mediaNumeros(temp))
			
			numeros = list(set(numeros))

			resultados.append(intersecao(proximo.numeros, numeros, True))	
			valido = intersecao(proximo.numeros, numeros, True) > 0

			
			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'resultados': resultados[-10:],
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarMediaDiferentesNoProximo.__code__.co_varnames[1:self.verificarMediaDiferentesNoProximo.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	
	def verificarMediaSerUmaDasPosicoes(self, tamanho = 1, posicoes = [1], posicoes2 = [0], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		resultados = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1
				
			numeros = []
			for a in anteriores:
				media = mediaNumeros(pegarPosicoes(a.numeros, posicoes))
				numeros.append(media)
				media = mediaNumeros(pegarPosicoes(a.numeros, posicoes2))
				numeros.append(media)

			media = mediaNumeros(pegarPosicoes(proximo.numeros, posicoes))
			numeros.append(media)
			media = mediaNumeros(pegarPosicoes(proximo.numeros, posicoes2))
			numeros.append(media)

			numeros = list(set(numeros))

			resultados.append(intersecao(proximo.numeros, numeros, True))
			valido = intersecao(proximo.numeros, numeros, True) > 0

			
			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'resultados': resultados[-10:],
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarMediaSerUmaDasPosicoes.__code__.co_varnames[1:self.verificarMediaSerUmaDasPosicoes.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarChaveContinuaIntervalo(self, tamanho = 1, intervalo = 2, retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		resultados = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1
				
			chaves = []
			chaves_proximo = []
			for n in range(0, 16-intervalo):
				chaves_proximo.append(chavePosicoes(proximo.numeros, range(n, n+intervalo)))
				for a in anteriores:
					chaves.append(chavePosicoes(a.numeros, range(n, n+intervalo)))


			chaves = list(set(chaves))
			resultados.append(intersecao(chaves_proximo, chaves, True))
			valido = intersecao(chaves_proximo, chaves, True) > 4

			
			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'resultados': resultados[-10:],
			'min': min(resultados),
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarChaveContinuaIntervalo.__code__.co_varnames[1:self.verificarChaveContinuaIntervalo.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarPosicaoSomaValores(self, posicoes = [0], somas = [1,1,2], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		tamanho = 1
		resultados = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1
				
			valido = False
			for n in posicoes:
				n_proximo = proximo.numeros[n]
				numeros = [n_proximo + p for p in somas]
				valido = valido or intersecao(proximo.numeros, numeros, True) == 2# len(numeros)
		
			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarPosicaoSomaValores.__code__.co_varnames[1:self.verificarPosicaoSomaValores.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarPosicaoSomaValoresV2(self, posicoes = [0], somas = [1,1,2], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		tamanho = 1
		resultados = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1
				
			valido = True
			for n in posicoes:
				n_proximo = proximo.numeros[n]
				numeros = [n_proximo + p for p in somas]
				valido = valido and intersecao(proximo.numeros, numeros, True) == len(numeros)
		
			if valido:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarPosicaoSomaValores.__code__.co_varnames[1:self.verificarPosicaoSomaValores.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)

	def verificarChaveDiferencaAnterior(self, tamanho = 2, posicoes = [0], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		resultados = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1
				
			diferencas_ant = []
			diferencas_prox = []
			for n in posicoes:
				diferencas_ant.append(anteriores[0].numeros[n] - anteriores[-1].numeros[n])
				diferencas_prox.append(anteriores[-1].numeros[n] - proximo.numeros[n])
		
			
			if chaveNumeros(diferencas_prox) == chaveNumeros(diferencas_ant):
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarChaveDiferencaAnterior.__code__.co_varnames[1:self.verificarChaveDiferencaAnterior.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)


	def verificarRankqueamentoColunas(self, tamanho = 5, posicoes = [0], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		resultados = []
		for idx in range(tamanho, len(_sorteios)):
			anteriores, proximo = _sorteios[idx-tamanho:idx],_sorteios[idx]
			jogos_analisados += 1
				
			top_ranks = []
			for n in posicoes:
				ocorrencias = []
				for a in anteriores:
					ocorrencias.append(a.numeros[n])

				rank = ranquearListaNumeros(ocorrencias)
				top_ranks.extend(rank[-1:])
			
			top_ranks = list(set(top_ranks))
			
			if intersecao(proximo.numeros, top_ranks, True) > 1:
				self.setInvalido(proximo)
				qtd_igual +=1

		acerto =  round(1 - qtd_igual /  max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto,
			'kwargs': [[k,v] for (k,v) in locals().items() if k in self.verificarChaveDiferencaAnterior.__code__.co_varnames[1:self.verificarChaveDiferencaAnterior.__code__.co_argcount]]
		}
		if retornando: return retorno
		pprint.pp(retorno)


	
# ranquear as colunas a partir de certas posicoes, ver se o top1 dessas colunas esta presente no seguinte


		
##############################################################################################################################################################################
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
##############################################################################################################################################################################

class ValidacaoAnalise():
	media_coluna = []

	'''Deve retornar True, sempre que a regra for INVÁLIDA!'''
	@staticmethod
	def sequenciaRepetidaJogoAnterior(proximo : Sorteio, anterior : Sorteio, tamanho_sequencia = 5):
		resposta = True
		proximo.setSequencias(tamanho_sequencia)
		anterior.setSequencias(tamanho_sequencia)
		for sq_proximo in proximo.sequencias:
			for sq_anterior in anterior.sequencias:
				resposta = resposta and intersecao(sq_proximo, sq_anterior, True) == len(sq_proximo)
		
		return resposta
	
	@staticmethod
	def	compararSomaPosicoesPares(proximo : Sorteio, anterior : Sorteio):
		anterior.setSomaPosicoesPares()
		proximo.setSomaPosicoesPares()
		return anterior.soma_posicoes_pares == proximo.soma_posicoes_pares
	
	@staticmethod
	def	compararSomaPosicoesImpares(proximo : Sorteio, anterior : Sorteio):
		anterior.setSomaPosicoesImpares()
		proximo.setSomaPosicoesImpares()
		return anterior.soma_posicoes_impares == proximo.soma_posicoes_impares
	
	@staticmethod
	def	compararChavePosicoes(proximo : Sorteio, anterior : Sorteio, posicoes = [1,3,9,12]):
		ret =  chavePosicoes(anterior.numeros, posicoes) == chavePosicoes(proximo.numeros, posicoes)
		return ret
	
	@staticmethod
	def	compararChavePosicoesComAnterior(proximo : Sorteio, anterior : Sorteio, posicoes = [1,3,9,12]):
		numeros_posicao = [proximo.numeros[x] for x in posicoes]
		return intersecao(numeros_posicao, anterior.numeros, True) == len(numeros_posicao)
	
	@staticmethod
	def compararSomas(proximo : Sorteio, anterior : Sorteio):
		return anterior.soma == proximo.soma
	
	@staticmethod
	def compararMultiplicacoes(proximo : Sorteio, anterior : Sorteio):
		return anterior.multiplicacao == proximo.multiplicacao
				
	@staticmethod
	def compararCaracteristicas(proximo : Sorteio, anterior : Sorteio, caracteristicas = []):
		for carac in caracteristicas:
			if str(getattr(anterior, carac)) != str(getattr(proximo, carac)):
				return False
		
		return True
		
	@staticmethod
	def contarQuantidadeRepetida(proximo : Sorteio, anterior : Sorteio, minimo = 6, maximo = 13):
		return not intersecao(anterior.numeros, proximo.numeros, True) in range(minimo, maximo+1)
				
	@staticmethod
	def verificarPossibilidadePosicao(proximo : Sorteio, posicao = 0, minimo = 6, maximo = 13):
		return not proximo.numeros[posicao] in range(minimo, maximo+1)
	
	@staticmethod
	def verificarMaximaDiferencaVizinhos(proximo : Sorteio, minimo = 6, maximo = 13):
		return not maxDiferencaVizinhos(proximo.numeros) in range(minimo, maximo+1)
				
	@staticmethod
	def verificarTamanhoMaximoSequencia(proximo : Sorteio, minimo = 6, maximo = 13):
		return not maxSequencia(proximo.numeros) in range(minimo, maximo+1)
																					
	@staticmethod
	def compararSomaPrimosIgual(proximo : Sorteio, anterior : Sorteio):
		return anterior.soma_primos == proximo.soma_primos
	
	@staticmethod
	def verificarCaracteristica(proximo : Sorteio, caracteristica = '', minimo = 2, maximo = 8):
		return not getattr(proximo, caracteristica) in range(minimo, maximo+1)
	
	@staticmethod
	def verificarContem(proximo : Sorteio, lista = []):
		for s in lista:
			if intersecao(proximo.numeros, s, True) == len(s):
				return True
		
		return False
	
	@staticmethod
	def	compararChavesIntervalos(proximo : Sorteio, anterior : Sorteio, intervalo = 2):
		anterior.setChaveIntervalo(intervalo)
		proximo.setChaveIntervalo(intervalo)
		return anterior.getChaveIntervalo(intervalo) == proximo.getChaveIntervalo(intervalo)
	
	@staticmethod
	def compararDiferencaPosicaoSimples(proximo : Sorteio, anterior : Sorteio, passo = 1):
		diferenca_anterior, diferenca_proximo = [], []
		for p in range(0, 15-passo):
			diferenca_anterior.append(anterior.numeros[p+passo] - anterior.numeros[p])
			diferenca_proximo.append(proximo.numeros[p+passo] - proximo.numeros[p])
		
		return chaveNumeros(diferenca_anterior) == chaveNumeros(diferenca_proximo)

	@staticmethod
	def compararSomaPosicaoSimples(proximo : Sorteio, anterior : Sorteio, passo = 1):
		soma_anterior, soma_proximo = [], []
		for p in range(0, 15-passo):
			soma_anterior.append(anterior.numeros[p+passo] + anterior.numeros[p])
			soma_proximo.append(proximo.numeros[p+passo] + proximo.numeros[p])
		
		return chaveNumeros(soma_anterior) == chaveNumeros(soma_proximo)

	@staticmethod
	def compararOperacoesPosicoes(proximo : Sorteio, anterior : Sorteio, posicoes = [], operacoes = []):
		return resolver(posicoes, operacoes, anterior.numeros) == resolver(posicoes, operacoes, proximo.numeros)
	
	@staticmethod
	def compararOperacoesPosicoesV2(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [], operacoes = []):
		valido = False
		for a in anteriores:
			resolvido = reduzir25(resolver(posicoes, operacoes, a.numeros))
			valido = valido or resolvido in proximo.numeros
		return not valido
	
	@staticmethod
	def compararOperacoesPosicoesV3(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [], operacoes = []):
		valido = False
		for a in anteriores:
			resolvido = reduzir25(resolver(posicoes, operacoes, a.numeros))
			valido = valido or resolvido in proximo.numeros
		return valido
	
	@staticmethod
	def compararCombinacaoSorteios(proximo : Sorteio, aanterior : Sorteio, anterior : Sorteio, pos_sorteio1 = [], pos_sorteio2 = [], prt = False):
		numeros_aanterior = pegarPosicoes(aanterior.numeros, pos_sorteio1)
		numeros_anterior = pegarPosicoes(anterior.numeros, pos_sorteio2)
		numeros_combinados = list(set([*numeros_aanterior, *numeros_anterior]))
		
		rr = intersecao(numeros_combinados, proximo.numeros, True) == len(numeros_combinados)
		prt and print(numeros_combinados)
		return rr
	
	@staticmethod
	def compararCombinacaoSorteiosMultiplos(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [], prt = False):
		
		tamanho = len(anteriores)
		combinados = []
		for i in range(tamanho):
			combinados.extend(pegarPosicoes(anteriores[i].numeros, posicoes[i]))

		numeros_combinados = list(set(combinados))
		
		comum = intersecao(numeros_combinados, proximo.numeros)
		todos_encontrados = len(comum) == len(numeros_combinados)
		if prt and todos_encontrados:
			for i in range(tamanho):
				print(pegarPosicoes(anteriores[i].numeros, posicoes[i]), posicoes[i])
			print(comum)
		return todos_encontrados
	
	@staticmethod
	def verificarRepeticaoChave(proximo : Sorteio, anteriores = [], posicoes = []):
		chave_proximo = chavePosicoes(proximo.numeros, posicoes)
		for sorteio in anteriores:
			if chavePosicoes(sorteio.numeros, posicoes) == chave_proximo:
				return True
	
		return False
		
	@staticmethod
	def compararCaracteristicaPosicao(proximo : Sorteio, anterior : Sorteio, caracteristica = 'primos', posicoes = [0,1,2,3,4]):
		chave_anterior = str(getattr(anterior, caracteristica)) + chavePosicoes(anterior.numeros, posicoes)
		chave_proximo = str(getattr(proximo, caracteristica)) + chavePosicoes(proximo.numeros, posicoes)
		return chave_anterior == chave_proximo
	
	@staticmethod
	def compararOcorrenciasNumerosRecorrentes(proximo : Sorteio, anteriores : list[Sorteio]):
		numeros_recorrentes = buscarCombos(2, anteriores[-1].numeros, anteriores)
		return intersecao(numeros_recorrentes, proximo.numeros, True) == len(numeros_recorrentes)
	
	@staticmethod
	def compararOcorrenciaRank(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [], rank = None):
		if not rank: rank = ranquearOcorrencias(anteriores)
		posicoes_rank = pegarPosicoes(rank, posicoes)
		contem = intersecao(posicoes_rank, proximo.numeros, True) == len(posicoes_rank)
		return contem
	
	@staticmethod
	def compararChaveOperacaoPosicoes(proximo : Sorteio, anterior : Sorteio, posicoes : list = [], operandos = ['-']):
		chave_ant, chave_pro = '', ''
		for i in range(len(posicoes) - 1):
			operando = operandos[i]
			match operando:
				case '/':
					chave_ant += str(round(anterior.numeros[posicoes[i+1]] / anterior.numeros[posicoes[i]], 1)) + '.'
					chave_pro += str(round(proximo.numeros[posicoes[i+1]] / proximo.numeros[posicoes[i]], 1)) + '.'
				case '-':
					chave_ant += str(round(anterior.numeros[posicoes[i+1]] - anterior.numeros[posicoes[i]], 1)) + '.'
					chave_pro += str(round(proximo.numeros[posicoes[i+1]] - proximo.numeros[posicoes[i]], 1)) + '.'
				case '*':
					chave_ant += str(round(anterior.numeros[posicoes[i+1]] * anterior.numeros[posicoes[i]], 1)) + '.'
					chave_pro += str(round(proximo.numeros[posicoes[i+1]] * proximo.numeros[posicoes[i]], 1)) + '.'
				case '+':
					chave_ant += str(round(anterior.numeros[posicoes[i+1]] + anterior.numeros[posicoes[i]], 1)) + '.'
					chave_pro += str(round(proximo.numeros[posicoes[i+1]] + proximo.numeros[posicoes[i]], 1)) + '.'

		return chave_ant == chave_pro
	
	@staticmethod
	def compararFatoracaoIgual(proximo : Sorteio, lista_comparacao : list, ultimos_sorteios : list[Sorteio]):
		lista_atual = fatorarAnteriores(proximo, ultimos_sorteios)
		for i in range(len(lista_comparacao)):
			if chaveNumeros(lista_comparacao[i]) == chaveNumeros(lista_atual[i]):
				return True
		return False
	
	@staticmethod
	def verificarPosicaoESomaOutros(proximo : Sorteio, posicao = 10, qtd_soma = 2, tipo = '+'):
		buscado = proximo.numeros[posicao]
		for comb in combinations(range(15), qtd_soma):
			if tipo == '+':
				soma = somaPosicoes(proximo.numeros, comb)
			else:
				soma = 1
				for n in comb:
					soma *= proximo.numeros[n]

			if soma == buscado:
				return False
			
		return True

	@staticmethod
	def verificarCaracteristicasPosicao(proximo : Sorteio, anterior : Sorteio, posicoes = [0], posicoes_chave = []):
		chave_ant, chave_pro = chavePosicoes(anterior.numeros, posicoes_chave), chavePosicoes(proximo.numeros, posicoes_chave)
		for posicao in posicoes:
			chave_ant += 'P' if anterior.numeros[posicao] % 2 == 0 else 'I'
			chave_pro += 'P' if proximo.numeros[posicao] % 2 == 0 else 'I'

		return chave_ant == chave_pro
	
	@staticmethod
	def verificarCaracteristicasPosicaoV2(proximo : Sorteio, anterior : Sorteio, posicoes = [[0]], posicoes_chave = [], modo = ''):
		chave_ant, chave_pro = chavePosicoes(anterior.numeros, posicoes_chave), chavePosicoes(proximo.numeros, posicoes_chave)
		
		for posicao in posicoes:
			soma_ant, mult_ant, diff_ant = somaPosicoes(anterior.numeros, posicao), multiplicarPosicoes(anterior.numeros, posicao), anterior.numeros[posicao[-1]] - anterior.numeros[posicao[0]]
			soma_pro, mult_pro, diff_pro = somaPosicoes(proximo.numeros, posicao), multiplicarPosicoes(proximo.numeros, posicao), proximo.numeros[posicao[-1]] - proximo.numeros[posicao[0]]

			qtdp_ant = numerosPares(anterior.numeros, posicao)
			qtdp_pro = numerosPares(proximo.numeros, posicao)

			match modo:
				case '':
					chave_ant += 'P' if soma_ant % 2 == 0 else 'I' + 'D5' if soma_ant % 5 == 0 else 'N5'
					chave_pro += 'P' if soma_pro % 2 == 0 else 'I' + 'D5' if soma_pro % 5 == 0 else 'N5'
				case 'M1':
					chave_ant += 'P' if soma_ant % 2 == 0 else 'I' + str(qtdp_ant)
					chave_pro += 'P' if soma_pro % 2 == 0 else 'I' + str(qtdp_pro)
				case 'M2':
					chave_ant += 'D3' if soma_ant % 3 == 0 else 'N3' + 'D4' if soma_ant > mediaNumeros(anterior.numeros) == 0 else 'N4'
					chave_pro += 'D3' if soma_pro % 3 == 0 else 'N3' + 'D4' if soma_pro > mediaNumeros(proximo.numeros) == 0 else 'N4'

		return chave_ant == chave_pro
	
	@staticmethod
	def verificarFuncaoLista(proximo : Sorteio, posicoes = [0], operacoes = [], lista = []):
		num_prox = resolver(posicoes, operacoes, proximo.numeros)
		return num_prox not in lista
	
	@staticmethod
	def compararFatoracaoSorteiosAnteriores(qtd_iteracoes = 5, lista = []):
		_sorteios = lista
		analitico = dict()
		for n in range(qtd_iteracoes):
			analitico[str(n)] = {}

		for idx in range(qtd_iteracoes, len(_sorteios)):
			proximo = _sorteios[idx]
			anteriores = _sorteios[idx-qtd_iteracoes:idx]

			for i, ant in enumerate(anteriores):
				posicoes = []
				comuns = intersecao(ant.numeros, proximo.numeros)
				for c in comuns:
					pos = ant.numeros.index(c)
					posicoes.append(pos)

					conjunto_analitico = analitico[str(i)]
					if not conjunto_analitico.get(str(pos)):
						conjunto_analitico[str(pos)] = 0

					conjunto_analitico[str(pos)] += 1

		for n in range(qtd_iteracoes):
			analitico[str(n)] = dict(sorted(analitico[str(n)].items(), key=lambda x: x[1], reverse=True))

		return analitico
	
	@staticmethod
	def verificarUsandoFuncao(proximo : Sorteio, anteriores : list[Sorteio], tamanho = 3, crescente = False, posicoes_ordenados = [0,1,2,3,4,5,6,7,8,9], tamanho_minimo = 16):
		resultado = ValidacaoAnalise.compararFatoracaoSorteiosAnteriores(tamanho, anteriores)
		ultimos_sorteios = anteriores[-tamanho:]
		numeros_encontrados, tam_intersecoes, quantidades = [], [], []
		for pos_loop in posicoes_ordenados:
			if len(numeros_encontrados) >= tamanho_minimo: break
			for p in range(tamanho):
				ordenado = resultado[str(p)]
				ordenado = dict(sorted(ordenado.items(), key=lambda x: x[1], reverse = crescente))
				chaves_ordenadas = list(ordenado.keys())
				if len(chaves_ordenadas) <= pos_loop: continue
				chave = chaves_ordenadas[pos_loop]
				numeros_encontrados.append(ultimos_sorteios[p].numeros[int(chave)])
				# print(ultimos_sorteios[p].numeros)

			numeros_encontrados = list(set(numeros_encontrados))

		tam_intersecoes.append(len(numeros_encontrados))
		quantidades.append(intersecao(numeros_encontrados, proximo.numeros, True))

		return intersecao(numeros_encontrados, proximo.numeros, True) > 13
	
	@staticmethod
	def verificarUsandoFuncaoV2(proximo : Sorteio, anteriores : list[Sorteio], tamanho = 3, crescente = False, posicoes_ordenados = [0,1,2,3,4,5,6,7,8,9], tamanho_minimo = 16):
		resultado = ValidacaoAnalise.compararFatoracaoSorteiosAnteriores(tamanho, anteriores)
		ultimos_sorteios = anteriores[-tamanho:]
		numeros_encontrados, tam_intersecoes, quantidades = [], [], []
		for pos_loop in posicoes_ordenados:
			if len(numeros_encontrados) >= tamanho_minimo: break
			for p in range(tamanho):
				ordenado = resultado[str(p)]
				ordenado = dict(sorted(ordenado.items(), key=lambda x: x[1], reverse = crescente))
				chaves_ordenadas = list(ordenado.keys())
				if pos_loop >= len(chaves_ordenadas): continue
				chave = chaves_ordenadas[pos_loop]
				numeros_encontrados.append(ultimos_sorteios[p].numeros[int(chave)])
				# print(ultimos_sorteios[p].numeros)

			numeros_encontrados = list(set(numeros_encontrados))

		tam_intersecoes.append(len(numeros_encontrados))
		quantidades.append(intersecao(numeros_encontrados, proximo.numeros, True))
		
		return intersecao(numeros_encontrados, proximo.numeros, True) < 11
	
	@staticmethod
	def verificarUsandoRanking(proximo : Sorteio, anteriores : list[Sorteio], ultimos):
		
		resultado = ranquearOcorrencias(anteriores)
		
		numeros_ranqueados = resultado[-ultimos:]

		return intersecao(proximo.numeros, numeros_ranqueados, True) == ultimos
		
	@staticmethod
	def verificarUsandoRankingV2(proximo : Sorteio, anteriores : list[Sorteio], ultimos):
		
		resultado = ranquearOcorrencias(anteriores)
		
		numeros_ranqueados = resultado[-ultimos:]

		return intersecao(proximo.numeros, numeros_ranqueados, True) < 2
	
	@staticmethod
	def verificarPosicaoNumeros(proximo : Sorteio, posicoes = [], numeros = []):
		
		chave_numeros = chaveNumeros(numeros)
		chave_posicoes = chavePosicoes(proximo.numeros, posicoes)

		return chave_numeros == chave_posicoes
	
	@staticmethod
	def verificarSomaPosicoesQuantidade(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1,2], maximo : int = 0, minimo : int = 0):
		agrupamento = anteriores
		numeros = pegarPosicoes(proximo.numeros, posicoes)
		for sorteio in agrupamento:
			numeros.extend(pegarPosicoes(sorteio.numeros, posicoes))
		
		soma = sum(numeros)
		return soma > maximo or soma < minimo
	
	@staticmethod
	def compararNumerosEMultiplicador(proximo : Sorteio, numeros = [1,2,3], multiplicador = 2):
		if isinstance(multiplicador, int):
			multiplicador = [multiplicador]
		numeros_multiplicados = list(numeros)
		for n in multiplicador:
			numeros_multiplicados.extend([x * n for x in numeros])

		numeros_multiplicados = list(set(numeros_multiplicados))
		return intersecao(proximo.numeros, numeros_multiplicados, True) == len(numeros_multiplicados)

	@staticmethod
	def compararNumerosEConvergencia(proximo : Sorteio, numeros = [1,2,3]):
		numeros_convergendo = list(numeros)
		numeros_convergendo.extend([x + 0 for x in numeros])
		numeros_convergendo.extend([26 - x  for x in numeros])

		numeros_convergendo = list(set(numeros_convergendo))
		return intersecao(proximo.numeros, numeros_convergendo, True) == len(numeros_convergendo)

	@staticmethod
	def verificarOperacaoPosicoes(proximo : Sorteio, posicoes = [[2,1]], operacao = '-'):
		todas_operacoes = set()
		for posicao in posicoes:
			[p1, p2] = posicao
			resultado = resolver(posicao, [operacao], proximo.numeros)
			todas_operacoes.add(resultado)
		
		return len(todas_operacoes) == 1
	
	@staticmethod
	def verificarContemOperacaoPosicoes(proximo : Sorteio, posicoes = [0,1], operacoes = ['-']):
		valor = resolver(posicoes, operacoes, proximo.numeros)
		return valor in proximo.numeros
	
	@staticmethod
	def verificarNaoContemTodos(proximo : Sorteio, numeros = [0]):
		return intersecao(proximo.numeros, numeros, True) == len(numeros)
	
	@staticmethod
	def verificarContemAlgum(proximo : Sorteio, numeros = [0]):
		return intersecao(proximo.numeros, numeros, True) == 0
	
	@staticmethod
	def verificarContemSomaSubPosicoes(proximo : Sorteio, posicoes = [0,1], operacoes = []):
		sub = resolver(posicoes, operacoes[0], proximo.numeros)
		som = resolver(posicoes, operacoes[1], proximo.numeros)

		return sub in proximo.numeros and som in proximo.numeros
	
	@staticmethod
	def compaparaOperacaoPosicoesSorteioSeguinte(proximo : Sorteio, anterior : Sorteio, operacoes = [['-','+']], posicoes = [[2,1,0]]):
		
		resolvidos = list(set([resolver(p, operacoes[i], anterior.numeros) for i, p in enumerate(posicoes)]))

		for pos in posicoes:
			resolvidos.extend(pegarPosicoes(anterior.numeros, pos))

		resolvidos = list(set(resolvidos))
		
		return intersecao(proximo.numeros, resolvidos, True) == len(resolvidos)
	
	@staticmethod
	def verificarOperacaoPosicaoExata(proximo : Sorteio, posicoes = [], operacoes = [], posicao_buscada = 0):
		return resolver(posicoes, operacoes, proximo.numeros) == proximo.numeros[posicao_buscada]
	
	@staticmethod
	def verificarSubtracaoUnicoNumero(proximo : Sorteio, posicoes = []):
		resolvidos = []
		for idx in range(len(posicoes) - 1):
			resolvidos.append(resolver([posicoes[idx], posicoes[idx+1]], ['-'], proximo.numeros))

		return len(set(resolvidos)) == 1
	
	@staticmethod
	def verificarSomasPosicoesComProximo(proximo : Sorteio, anterior : Sorteio, posicoes = [0,3,5], evitar = 0):
		dif = somaPosicoes(proximo.numeros, posicoes) - somaPosicoes(anterior.numeros, posicoes)
		return dif == evitar
		
	@staticmethod
	def verificarFuncaoContemNumeroGerado(proximo : Sorteio, posicoes = [], equacao = ''):
		resolvido = resolverFuncao(posicoes, proximo.numeros, equacao)
		# print(equacao, resolvido)
		return resolvido not in proximo.numeros
		
	@staticmethod
	def verificarSorteiosCombinacoesNoRank(proximo : Sorteio, rank = [], posicoes = [0,3,5]):
		tamanho_posicoes = len(posicoes)
		ranqueado = rank
		
		chave_ranqueado = chaveNumeros(ranqueado[-tamanho_posicoes:])
		chave_numero = chavePosicoes(proximo.numeros, posicoes)
			
		return chave_ranqueado == chave_numero
	
	@staticmethod
	def verificarPropriedadeNosIntervalos11(proximo : Sorteio, propriedade = '', min_max = [0,0]):
		sorteios_menores = [gerarSorteioSimples(proximo.numeros[x:x+11]) for x in range(0,5)]
		for sorteio in sorteios_menores:
			prop = getattr(sorteio, propriedade)
			if prop < min_max[0] or prop > min_max[1]: return True
		
		return False
	
	@staticmethod
	def verificarCombinacoesEntreSorteios(proximo : Sorteio, anterior : Sorteio):
		combinacoes = []
		for c in combinations(range(15), 13):
			combinacoes.append(chavePosicoes(anterior.numeros, c))
			combinacoes.append(chavePosicoes(proximo.numeros, c))

		total_unicos = len(list(set(combinacoes)))
		
		return total_unicos != 210
	
	@staticmethod
	def verificarCaracteristicaSubSorteioSorteios(proximo : Sorteio, tamanho = 11, caracteristica = 'pares', igual = True):
		caracteristicas = []
		sorteios_menores = [gerarSorteioSimples(proximo.numeros[x:x+tamanho]) for x in range(16-tamanho)]
		for s in sorteios_menores:
			caracteristicas.append(getattr(s, caracteristica))

		total_unicos = len(list(set(caracteristicas)))
		
		return total_unicos != 1 if not igual else total_unicos == 1
	
	@staticmethod
	def verificarQuantidadeNoRank(proximo : Sorteio, anteriores : list[Sorteio]):
		
		ranqueado = ranquearOcorrencias(anteriores)
		for c in [ranqueado[0:5], ranqueado[5:10], ranqueado[10:15], ranqueado[15:20], ranqueado[20:25]]:
			qtd_comum = intersecao(c, proximo.numeros, True)
			if qtd_comum == 0: return True

		for c in [ranqueado[0:8], ranqueado[8:16], ranqueado[16:]]:
			qtd_comum = intersecao(c, proximo.numeros, True)
			if qtd_comum < 2 or qtd_comum > 8: return True

		return False
	
	@staticmethod
	def verificarNumeroPosicaoCaracteristicas(proximo : Sorteio, anterior : Sorteio, posicoes = [0, 1], posicoes_caracteristica = [3,4]):
		
		posicoes_iguais = chavePosicoes(anterior.numeros, posicoes) == chavePosicoes(proximo.numeros, posicoes)
		posicoes_caracteristica_iguais = chaveImPa(anterior.numeros, posicoes_caracteristica) == chaveImPa(proximo.numeros, posicoes_caracteristica)

		return posicoes_iguais and posicoes_caracteristica_iguais

	@staticmethod
	def verificarNumeroPosicaoNumeroNao(proximo : Sorteio, anterior : Sorteio, posicoes = [0, 1]):
		
		chave_atual = chavePosicoes(anterior.numeros, posicoes)
		chave_proximo = chavePosicoes(proximo.numeros_nao, posicoes)

		return chave_atual == chave_proximo
	
	@staticmethod
	def verificarNumerosInversoAnterior(proximo : Sorteio, anteriores = list[Sorteio]):
		temp = [*anteriores[0].numeros]
		temp.reverse()
		ant_01 = temp
		ant_02 = anteriores[-1].numeros

		subs = []
		for i in range(8):
			subs.append(ant_01[i] - ant_02[i])

		diferentes = list(set(subs))
		comuns = intersecao(proximo.numeros, diferentes, True)
		
		return comuns == len(diferentes)
	
	@staticmethod
	def analisarCalcularMediaColunas(proximo : Sorteio, anteriores : list[Sorteio]):
		if len(ValidacaoAnalise.media_coluna) == 0:
			soma = []
			analise = Analise(anteriores)

			for n in range(15):
				ret = analise.calcularMediaColunas(2, n, anteriores, True)
				soma.append(abs(ret['media'] - anteriores[-1].numeros[n]))

			ValidacaoAnalise.media_coluna = soma

		comum = intersecao(proximo.numeros, ValidacaoAnalise.media_coluna, True)
		resultado = comum < 5 or comum > 10
		# if resultado:
		# 	print(comum)
		return resultado

	@staticmethod
	def verificarSomaDiferencasEsqDir(proximo : Sorteio, posicoes = [], possiveis = []):
		for n in posicoes:
			comum = proximo.numeros[n] - proximo.numeros[n-1] + proximo.numeros[n+1] - proximo.numeros[n]

			if comum not in possiveis:
				return True
			
		return False
	
	@staticmethod
	def verificarSequenciaLinhas(proximo : Sorteio, caminho : str, anteriores : list[Sorteio], posicoes = [1,2,3,4]):
	
		novo = []
		novo.extend(anteriores)
		novo.append(proximo)
		encontrados = buscarNumerosCaminho(novo, posicoes, caminho)
		encontrados.sort()
			
		sequencia_valida = True
		for i in range(len(encontrados) - 1):
			sequencia_valida = sequencia_valida and (encontrados[i] == (encontrados[i+1] - 1))

		return sequencia_valida
	
	@staticmethod
	def verificarSomaDifencaMaior1(proximo : Sorteio):
		soma = []
		for n in range(1, 15):
			dif = proximo.numeros[n] - proximo.numeros[n-1]
			ret = dif if dif > 1 else 0
			soma.append(ret)

		return sum(soma) < 10
	
	@staticmethod
	def verificarDistanciasNumeros(proximo : Sorteio):
	
		iguais = True
		for n in range(7):
			minimo = proximo.numeros[n] - 1
			maximo = 25 - proximo.numeros[14-n]
			iguais = iguais and minimo == maximo

		return iguais
	
	@staticmethod
	def	compararChaveSequenciaPulo(proximo : Sorteio, anterior : Sorteio):
		chave_anterior = chaveSequenciaPulo(anterior.numeros)
		chave_proximo = chaveSequenciaPulo(proximo.numeros)
		return chave_anterior == chave_proximo
	
	@staticmethod
	def	verificarChavesPuloRepetido(proximo : Sorteio):
		todas = todasSequenciasPulos(proximo.numeros)
		return  len(todas) < 2

	@staticmethod
	def	verificarQuantidadeIrmaos(proximo : Sorteio):
		todas = quantidadeNumerosIrmaos(proximo.numeros)
		return todas < 6
		

	@staticmethod
	def verificarSequenciaPar(proximo : Sorteio):
		return len(todasSequenciasPares(proximo.numeros, True)) > 3 or len(todasSequenciasPares(proximo.numeros)) > 3
		

	@staticmethod
	def verificarNumeroxCaracteristica(proximo : Sorteio, numero = 1, mapa = {}):
		if numero not in proximo.numeros: return False

		for (caracteristica, aceitaveis) in mapa.items():
			valor = getattr(proximo, caracteristica)
			if valor not in aceitaveis:
				# print(numero, caracteristica, valor)
				return True
			
		return False
	
	@staticmethod
	def verificarSorteioComCrescimento(proximo : Sorteio, crescimento = [1,2,3,4]):
		return contemSquenciaCrescente(proximo.numeros, crescimento)
	
	@staticmethod
	def verificarSomaUnicaPosicoes(proximo : Sorteio, posicoes = [0,1,2,3]):
		todas_somas = []
		for i in range(len(posicoes)):
			pos = posicoes[i]
			pos_fim = posicoes[len(posicoes) - 1 -i]
			soma = proximo.numeros[pos] + proximo.numeros[pos_fim]
			todas_somas.append(soma)

		tamanho = len(list(set(todas_somas)))

		return tamanho == 1

	@staticmethod
	def verificarNumeroxCaracteristicaPosicoes(proximo : Sorteio, numero = 1, posicoes = [0], evitar = '', tipo = 'padrao'):
		if numero not in proximo.numeros: return False

		soma = ''
		if tipo == 'padrao':
			for posicao in posicoes:
				soma += 'P' if proximo.numeros[posicao] % 2 == 0 else 'I'
		elif tipo == 'extra':
			soma = str(proximo.quantidade_menores_6) + '.' + str(proximo.quantidade_menores_18)
		elif tipo == 'soma':
			soma = str(sum([proximo.soma_meio, proximo.quantidade_menores_18])) + '.' + str(sum([proximo.pares, proximo.soma_menores_13])) + '.' + str(sum([proximo.soma_entre_10_20, proximo.quantidade_maiores_20]))
		elif tipo == 'mods':
			soma += str(int((proximo.quantidade_menores_10) % somaPosicoes(proximo.numeros, posicoes))) + '.' + str(proximo.pares)
		elif tipo == 'mods2':
			soma += str(int(proximo.soma / somaPosicoes(proximo.numeros, posicoes))) + '.'
		else:
			for posicao in posicoes:
				soma += 'P' if proximo.numeros[posicao] % 2 == 0 else 'I'
			for n in [proximo.pares]:
				soma += str(n)
				
			

		return soma == evitar

	@staticmethod
	def verificarNumeroxCaracteristicaColuna(proximo : Sorteio, anteriores = list[Sorteio], coluna = 0, evitar = '', tipo = 'padrao', mods = []):
		lista = [*anteriores]
		lista.append(proximo)
		numeros = [s.numeros[coluna] for s in lista]
		if tipo == 'padrao':
			soma = ''
			xx = 1
			for num in numeros:
				xx *= num
				soma += 'P' if xx % 2 == 0 else 'I'
		elif tipo == 'mods':
			soma = ''
			for n in [3,7]:
				soma += str(sum(numeros) % n) + '.'
		elif tipo == 'mods2':
			soma = ''
			for n in [5,8,11]:
				soma += str(sum(numeros) % n) + '.'
		elif tipo == 'dinamico':
			soma = ''
			for n in mods:
				soma += str(sum(numeros) % n) + '.'

		# if (soma == evitar):
		# 	print(soma, evitar, coluna, numeros, sum(numeros), proximo.numeros)
		return soma == evitar
	
	@staticmethod
	def validarExecoesFuncoes(proximo : Sorteio, lista_funcoes = []):
		contem_todos = True
		for [fn, pos] in lista_funcoes:
			num = resolverFuncao(pos, proximo.numeros, fn)
			contem_todos &= num in proximo.numeros

		return contem_todos


	@staticmethod
	def verificarNumerosxSomas(proximo : Sorteio, posicoes = 0, anteriores = [], tipo = 'padrao', mods = [], evitar = ''):
		lista = [*anteriores]
		lista.append(proximo)

		numeros = []
		numeros_nao = []
		for (i, s) in enumerate(lista):
			posi = posicoes[i]
			numeros.append(s.numeros[posi])
			if posi < 10:
				numeros_nao.append(s.numeros_nao[posi])
		
		soma = ''
		if tipo == 'diffs':
			for i in range(1, len(numeros)):
				soma += str(abs(numeros[i] - numeros[i-1]))

		if tipo == 't01':
			for i in range(1, len(numeros_nao)):
				soma += str(abs(numeros_nao[i] - numeros_nao[i-1]))
		
		if tipo == 't02':
			for i in range(1, len(numeros_nao)):
				soma += str(abs(numeros_nao[i] - numeros_nao[i-1]))
			for i in range(1, len(numeros)):
				soma += str(abs(numeros[i] - numeros[i-1]))

		if tipo == 't03':
			for s in lista:
				soma += str(s.quantidade_menores_6)
				
		# print(soma, evitar)
		return soma == evitar
	
	@staticmethod
	def verificarNumerosPosicoesAnteriores(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0, 1]):
		
		_lista = [*anteriores, proximo]
		numeros_anteriores = []
		for (i, s) in enumerate(_lista):
			numeros_anteriores.append(s.numeros[posicoes[i]])

		chave_anterior = chaveNumeros(numeros_anteriores)
		chave_proximo = chavePosicoes(proximo.numeros, posicoes)
			
		return chave_anterior == chave_proximo
	

	@staticmethod
	def verificarChavePossivel(proximo : Sorteio, numeros = [1], caracteristicas = ['pares', 'quantidade_menores_10'], evitar = ['']):
		
		if intersecao(proximo.numeros, numeros, True) != len(numeros): return False
		
		chave = []
		for c in caracteristicas:
			chave.append(str(getattr(proximo, c)))

		chave_str = '.'.join(chave)

		return chave_str in evitar
	
	@staticmethod
	def verificarUltimosTodosNumeros(proximo : Sorteio, anteriores : list[Sorteio], intervalo = [0,2], qtd_buscada = 4):
		_lista = [*anteriores, proximo]
		numeros_anteriores = []
		for s in _lista:
			numeros_anteriores.extend(s.numeros[intervalo[0]:intervalo[1]])

		numeros_encontrados = list(set(numeros_anteriores))
		qtd_numeros = len(numeros_encontrados)
		tem_sequencia = len(obterTodasSequencias(numeros_encontrados, qtd_buscada)) != 0
		return qtd_numeros == qtd_buscada
	
	@staticmethod
	def compararChaveQuantidadeDistintosIntervalo(proximo : Sorteio, anteriores : list[Sorteio], intervalo = 2):
		chave_anterior = []
		chave_atual = []
		for i in range(15-intervalo):
			n_ant = []
			n_atu = []
			for (p, a) in enumerate(anteriores):
				n_ant.extend(a.numeros[i:i+intervalo])
				if p > 0:
					n_atu.extend(a.numeros[i:i+intervalo])
					n_atu.extend(proximo.numeros[i:i+intervalo])
					
			chave_anterior.append(str(len(list(set(n_ant)))))
			chave_atual.append(str(len(list(set(n_atu)))))

		chave_atual = '.'.join(chave_atual)
		chave_anterior = '.'.join(chave_anterior)

		return chave_anterior == chave_atual
	
	@staticmethod
	def compararChaveQuantidadeIguaisIntervalo(proximo : Sorteio, anteriores : list[Sorteio], intervalo = 2):
		chave_anterior = []
		chave_atual = []
		for i in range(15-intervalo):
			n_ant = list(range(1,26))
			n_atu = list(range(1,26))
			for (p, a) in enumerate(anteriores):
				n_ant = intersecao(a.numeros[i:i+intervalo], n_ant)
				if p > 0:
					n_atu = intersecao(a.numeros[i:i+intervalo], n_atu)
					n_atu = intersecao(proximo.numeros[i:i+intervalo], n_atu)
			
			chave_anterior.append(str(len(n_ant)))
			chave_atual.append(str(len(n_atu)))
		
		chave_atual = '.'.join(chave_atual)
		chave_anterior = '.'.join(chave_anterior)

		return chave_anterior == chave_atual
	
	@staticmethod
	def compararChaveSomaPosicoes(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [[0,1],[1,2]]):
		
		chave_anterior = []
		chave_atual = []
		
		total = 0
		for (p, a) in enumerate(anteriores):
			total += somaPosicoes(a.numeros, posicoes[p])
		chave_anterior.append(str(total))
			
		chave_atual.append(str(somaPosicoes(proximo.numeros, posicoes[-1])))
					
		chave_atual = '.'.join(chave_atual)
		chave_anterior = '.'.join(chave_anterior)

		tem_comum = intersecao(pegarPosicoes(anteriores[0].numeros, posicoes[0]), pegarPosicoes(proximo.numeros, posicoes[1]), True) > 0
		# pprint.pp({
		# 	'po': posicoes,
		# 	'cn': chave_anterior,
		# 	'ca': chave_atual,
		# 	'tc': tem_comum,
		# 	'pn': proximo.numeros
		# })
		return chave_anterior == chave_atual and tem_comum
	

	@staticmethod
	def verificarSomaPosicoesPresenteProximo(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,2]):

		somas = []
		for s in anteriores:
			somas.append(somaPosicoes(s.numeros, posicoes))

		somas = list(set([(soma % 25) + 1 for soma in somas]))
		return intersecao(somas, proximo.numeros, True) == len(somas)
	
	@staticmethod
	def verificarSomaPosicoesAlgumPresenteProximo(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,2]):
		
		somas = []
		for s in anteriores:
			somas.append(somaPosicoes(s.numeros, posicoes))

		somas = list(set([(soma % 25) + 1 for soma in somas]))
		iguais = intersecao(somas, proximo.numeros, True)

		# print(posicoes, somas, intersecao(somas, proximo.numeros))
		return iguais == 0
	
	@staticmethod
	def verificarAlgumaChaveAnteriores(proximo : Sorteio, anteriores : list[Sorteio], caracteristicas = ['pares', 'quantidade_menores_10']):
		
		chaves = []
		chaves_proximo = []
		for c in caracteristicas:
			chaves_proximo.append('.'.join([c, str(getattr(proximo, c))]))
			for a in anteriores:
				chaves.append('.'.join([c, str(getattr(a, c))]))

		
		return intersecao(chaves_proximo, chaves, True) == 0
	
	@staticmethod
	def verificarNenhumaChaveAnteriores(proximo : Sorteio, anteriores : list[Sorteio], caracteristicas = ['pares', 'quantidade_menores_10']):
		chaves = []
		chaves_proximo = []
		for c in caracteristicas:
			chaves_proximo.append('.'.join([c, str(getattr(proximo, c))]))
			for a in anteriores:
				chaves.append('.'.join([c, str(getattr(a, c))]))

		
		return intersecao(chaves_proximo, chaves, True) == len(caracteristicas)
	
	@staticmethod
	def verificarContemTodasSomas(proximo : Sorteio, anteriores : list[Sorteio], tamanho_somas = 2, quantidade_buscada = 0):
		
		somas = []
		for n in range(0, 16 - tamanho_somas, tamanho_somas):
			for a in anteriores:
				soma = (sum(a.numeros[n:n+tamanho_somas]) % 25) + 1
				somas.append(soma)

		somas = list(set(somas))
		return intersecao(somas, proximo.numeros, True) == quantidade_buscada
	
	@staticmethod
	def verificarContemAlgumaChave(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1,2]):
		chaves = []
		for a in anteriores:
			soma = sum(pegarPosicoes(a.numeros, posicoes))
			for sm in range(soma-5, soma+6):
				chaves.append(sm)

		chave_proximo = sum(pegarPosicoes(proximo.numeros, posicoes))
		
		# print(chaves, chave_proximo)
		return chave_proximo not in chaves
	
	@staticmethod
	def verificarContemTodosNumeros(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1], buscado = 0):
		numeros = []
		for (i,a) in enumerate(anteriores):
			numeros.append(a.numeros[posicoes[i]])
		
					
		return intersecao(proximo.numeros, numeros, True) == buscado
	
	@staticmethod
	def verificarContemTodosNumerosFuncao(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1,2], buscado = 3):
		
		numeros = []
		resultado = []
		for (i,a) in enumerate(anteriores):
			numeros.append(a.numeros[posicoes[i]])
			resultado.append(sum(pegarPosicoes(a.numeros, posicoes)))

		#, sum(numeros), multiplicarPosicoes(numeros, range(tamanho))]
		resultado = list(set([(x % 25) + 1 for x in resultado]))
		
		return intersecao(proximo.numeros, resultado, True) in range(buscado-2,buscado+1)
	
	@staticmethod
	def verificarChavesGrupos(proximo : Sorteio, anteriores : list[Sorteio], inicio = 1, fim = 13):		
		resultado = []
		for (i,a) in enumerate(anteriores):
			resultado.append(chaveDiferencaRange(a.numeros, inicio, fim))

		resultado = list(set(resultado))
		
		chave_proximo = chaveDiferencaRange(proximo.numeros, inicio, fim)

		return chave_proximo in resultado

	@staticmethod
	def verificarPosicoesAlgumPresenteMesmaProximo(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,2], buscado = 3):
		contador = 0
		for s in anteriores:
			contador += 1 if intersecao(pegarPosicoes(s.numeros, posicoes), proximo.numeros, True) == buscado else 0

		return contador > 0
	
	@staticmethod
	def verificarPosicoesPresenteSalto(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,2]):
		
		valido = False
		for s in anteriores:
			if intersecao(pegarPosicoes(s.numeros, posicoes), proximo.numeros, True) == len(posicoes):
				valido = True

		return not valido
	
	@staticmethod
	def verificarChavesSomaIntervaloAlgumPresenteProximo(proximo : Sorteio, anteriores : list[Sorteio], intervalo = 3):

		possibilidades = []
		for s in anteriores:
			possibilidades.append(chaveSomaPulando(s.numeros, intervalo))

		possibilidades_proximo = [
			chaveSomaPulando(proximo.numeros, intervalo)
		]

		return intersecao(possibilidades, possibilidades_proximo, True) > 0
	
	@staticmethod
	def verificarSomaColunasPresenteProximo(proximo : Sorteio, anteriores : list[Sorteio], colunas = [2,3,4]):
	
		possibilidades = [0 for x in colunas]
		for (p,coluna) in enumerate(colunas):
			for s in anteriores:
				possibilidades[p] += s.numeros[coluna]

		possibilidades = [
			(n % 25) + 1 for n in possibilidades
		]

		return intersecao(possibilidades, proximo.numeros, True) == 0
	
	@staticmethod
	def verificarUmPorSorteioAnteriorInvertida(proximo : Sorteio, anteriores : list[Sorteio], colunas = [0,1,2,3]):
		valido = True
		c2 = list(colunas)
		c2.reverse()
		for (p,coluna) in enumerate(c2):
			valido = valido and (proximo.numeros[coluna] in anteriores[p].numeros)

		return valido
	
	@staticmethod
	def verificarUmPorSorteioAnterior(proximo : Sorteio, anteriores : list[Sorteio], colunas = [0,1,2,3]):
		valido = True
		c2 = list(colunas)
		for (p,coluna) in enumerate(c2):
			valido = valido and (proximo.numeros[coluna] in anteriores[p].numeros)

		return valido
	
	@staticmethod
	def verificarUmPorSorteioAnteriorAmbas(proximo : Sorteio, anteriores : list[Sorteio], colunas = [0,1,2,3]):
		valido = True
		for (p,coluna) in enumerate(colunas):
			valido = valido and (proximo.numeros[coluna] in anteriores[p].numeros)

		c2 = list([*colunas])
		c2.reverse()
		for (p,coluna) in enumerate(c2):
			valido = valido and (proximo.numeros[coluna] in anteriores[p].numeros)

		return valido 
	
	@staticmethod
	def verificarSomaPosicoesNoAnterior(proximo : Sorteio, anteriores : list[Sorteio], intervalo = 2, buscado = 2):
		numeros = []
		for i in range(0, 15 - intervalo):
			numeros.append((sum(proximo.numeros[i:i+intervalo]) % 25) + 1)
		
		numeros = list(set(numeros))

		quantidade = intersecao(numeros, proximo.numeros, True)
		comuns = proximo.numeros
		for s in anteriores:
			comuns = intersecao(comuns, s.numeros)

		quantidade_comuns = len(comuns)

		return quantidade == buscado and quantidade_comuns == buscado
	
	@staticmethod
	def verificarChaveIntersecaoSomas(proximo : Sorteio, anteriores : list[Sorteio], intervalos = [[0,7],[8,15]]):
		
		quantidades = []
		quantidades_proximo = []
		for [i,f] in intervalos:
			temp = list(range(25))
			temp_proximo = proximo.numeros[i:f]
			for a in anteriores:
				temp = intersecao(temp, a.numeros[i:f])
			
			for a in anteriores[1:]:
				temp_proximo = intersecao(temp_proximo, a.numeros[i:f])
			
			quantidades.append(len(temp))
			quantidades_proximo.append(len(temp_proximo))
		
		chave_ant = '.'.join([str(x) for x in quantidades])
		chave_prox = '.'.join([str(x) for x in quantidades_proximo])

		# print(quantidades, chave_ant)
		# print(quantidades_proximo, chave_prox)
		# exit()

		return chave_ant == chave_prox
	
	@staticmethod
	def verificarIntersecaoContemMinimo(proximo : Sorteio, anteriores : list[Sorteio], intervalos = [[0,7],[8,15]]):
		quantidades_proximo = []
		for [i,f] in intervalos:
			quantidades_proximo.append(intersecao(proximo.numeros[i:f], anteriores[0].numeros[i:f], True))
		
		todos_maior = [x for x in quantidades_proximo if x > 3]
		return len(todos_maior) == len(quantidades_proximo)

	@staticmethod
	def verificarSomaNaoPresentesNoProximo(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1]):
		somas = []
		for a in anteriores:
			somas.append(sum(pegarPosicoes(a.numeros_nao, posicoes)) % 25 + 1)
		
		somas = list(set(somas))

		alguma_carac = True
		for c in ['pares', 'quantidade_menores_12']:
			alguma_carac = alguma_carac and getattr(proximo, c) == getattr(anteriores[-1], c)

		return intersecao(somas, proximo.numeros, True) == len(somas) and alguma_carac
	
	@staticmethod
	def verificarCaracteristicasMinimasPresentesNoProximo(proximo : Sorteio, anteriores : list[Sorteio], caracteristicas = ['pares']):
		alguma_carac = False
		for c in caracteristicas:
			for a in anteriores:
				alguma_carac = alguma_carac or getattr(proximo, c) == getattr(a, c)

		return not alguma_carac
	
	@staticmethod
	def verificarModuloDiferencaPresentesNoProximo(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1], caracteristicas = ['pares']):

		diferencas = []
		for a in anteriores:
			diferencas.append(abs(sum(pegarPosicoes(a.numeros, posicoes)) - sum(pegarPosicoes(proximo.numeros, posicoes))) % 25 + 1)
		
		diferencas = list(set(diferencas))

		valido = 0
		for c in caracteristicas:
			for a in anteriores:
				valido += 1 if getattr(proximo, c) == getattr(a, c) else 0

		invalido = intersecao(diferencas, proximo.numeros, True) == 0 and valido > 3
		return invalido
	
	@staticmethod
	def verificarProximoNosAnteriores(proximo : Sorteio, anteriores : list[Sorteio], buscado = 15):

		novos = []
		for a in anteriores:
			novos.extend(a.numeros)

		return len([x for x in novos if x in proximo.numeros]) == buscado
	
	@staticmethod
	def verificarProximoQuantidadeNosAnteriores(proximo : Sorteio, anteriores : list[Sorteio], buscado = 15):
		valido = False
		for a in anteriores:
			valido = valido or intersecao(a.numeros, proximo.numeros, True) == buscado

		return valido
	
	@staticmethod
	def verificarProximoCaracteristicaseNosAnteriores(proximo : Sorteio, anteriores : list[Sorteio], caracteristicas = ['pares']):
		carac_proximo = []
		for c in caracteristicas:
			carac_proximo.append(str(getattr(proximo, c)))
		carac_proximo = '.'.join(carac_proximo)

		valido = False
		for a in anteriores:
			carac_atual = []
			for c in caracteristicas:
				carac_atual.append(str(getattr(a, c)))
				
			carac_atual = '.'.join(carac_atual)
			valido = valido or carac_atual == carac_proximo

		return valido
	
	@staticmethod
	def analiseChaveDiferencaProximo(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1,2]):
		ch_temp = []
		ch_temp_prox = []
		for p in posicoes:
			ch_temp.append(str(abs(anteriores[0].numeros[p] - anteriores[1].numeros[p])))
			ch_temp_prox.append(str(abs(anteriores[-1].numeros[p] - proximo.numeros[p])))
		ch_temp = '.'.join(ch_temp)
		ch_temp_prox = '.'.join(ch_temp_prox)

	
		return ch_temp == ch_temp_prox
	
	@staticmethod
	def verificarDeslocamentoPosicoes(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1]):
		
		chave_anterior = chavePosicoes(anteriores[0].numeros, posicoes)
		chave_proximo = chavePosicoes(proximo.numeros, [x+1 for x in posicoes])
		
		return chave_anterior == chave_proximo
	
	@staticmethod
	def verificarRepeticaoChaveDiferenca(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0, 15]):
	
		chave_anterior = []
		chave_proximo = []

		for (p, n) in enumerate(posicoes):
			if p == len(posicoes) - 1: continue
			chave_anterior.append(anteriores[0].numeros[posicoes[p+1]] - anteriores[0].numeros[posicoes[p]])
			chave_proximo.append(proximo.numeros[posicoes[p+1]] - proximo.numeros[posicoes[p]])
		
		return chave_anterior == chave_proximo
	
	@staticmethod	
	def verificarRepeticaoPorPosicao(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0, 1]):
		
		quantidade_repetida = 0
		
		for a in anteriores:
			quantidade_repetida += intersecao(pegarPosicoes(a.numeros, posicoes), pegarPosicoes(proximo.numeros, posicoes), True)
		
		return not quantidade_repetida > 0
	
	@staticmethod
	def verificarRepeticaoPorPosicaoComQuantidade(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0, 1], buscado = 1):
		quantidade_repetida = 0
		
		for a in anteriores:
			quantidade_repetida += intersecao(pegarPosicoes(a.numeros, posicoes), pegarPosicoes(proximo.numeros, posicoes), True)
		
		return quantidade_repetida == buscado
	
	@staticmethod
	def verificarRepeticaoPorPosicaoComQuantidadeDiferente(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0, 1], buscado = 1):
		quantidade_repetida = 0
		
		for a in anteriores:
			quantidade_repetida += intersecao(pegarPosicoes(a.numeros, posicoes), pegarPosicoes(proximo.numeros, posicoes), True)
		
		return not quantidade_repetida != buscado
	
	@staticmethod
	def verificarRepeticaoPorPosicaoAnterioresComQuantidadeDiferente(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0, 1], buscado = 1):

		quantidade_repetida = 0
		
		for a in anteriores:
			quantidade_repetida += intersecao(pegarPosicoes(a.numeros, posicoes), proximo.numeros, True)
		
		return not quantidade_repetida != buscado
	
	@staticmethod
	def verificarGapsPresentesSeguinte(proximo : Sorteio, anteriores : list[Sorteio]):
		valido = False
		entrou = False
		for i in range(1, 15):
			inicio = anteriores[0].numeros[i-1]
			fim = anteriores[0].numeros[i]
			if fim - inicio < 3: continue
			valido = valido or intersecao(proximo.numeros, list(range(inicio, fim+1)), True) > 0
			entrou = True
		
		if not entrou:
			valido = True

		return not valido
		
	@staticmethod
	def verificarTodosGapsPresentesSeguinte(proximo : Sorteio, anteriores : list[Sorteio], buscado = 2):
		numeros = []
		for a in anteriores:
			for i in range(1, 15):
				inicio = a.numeros[i-1]
				fim = a.numeros[i]
				if fim - inicio < 2: continue
				numeros.append(inicio)
				numeros.append(fim)
		
		numeros = list(set(numeros))
		numeros_comuns = intersecao(proximo.numeros, numeros, True) 
		
		return buscado == numeros_comuns

	@staticmethod
	def verificarSomaPresenteSeguinte(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1,2], somas = [0,0,0]):
		numeros = []
		for a in anteriores:
			for (p,v) in enumerate(somas):
				numeros.append(a.numeros[posicoes[p]] + somas[p])
		
		numeros = list(set(numeros))
		numeros_comuns = intersecao(proximo.numeros, numeros, True) 
		return len(numeros) == numeros_comuns
	
	@staticmethod
	def verificarSomaMinimaPresenteSeguinte(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1,2], somas = [0,0,0], minimo = 3):
		numeros = []
		for a in anteriores:
			for (p,v) in enumerate(somas):
				numeros.append(a.numeros[posicoes[p]] + somas[p])
		
		numeros = list(set(numeros))
		numeros_comuns = intersecao(proximo.numeros, numeros, True) 
		return numeros_comuns > minimo
	
	@staticmethod
	def verificarSomaMinimaIgualPresenteSeguinte(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1,2], somas = [0,0,0], minimo = 3):
		numeros = []
		for a in anteriores:
			for (p,v) in enumerate(somas):
				numeros.append(a.numeros[posicoes[p]] + somas[p])
		
		numeros = list(set(numeros))
		numeros_comuns = intersecao(proximo.numeros, numeros, True) 
		return not numeros_comuns >= minimo
	
	@staticmethod
	def verificarSomaSequencialNaoTemTodosSeguinte(proximo : Sorteio, anteriores : list[Sorteio], somas = [0,0,0], minimo = 15):
		
		numeros = []
		for a in anteriores:
			for i in range(0, 15 - len(somas), len(somas)):
				for (p, v) in enumerate(somas):
					numeros.append((abs(a.numeros[i + p] + v) % 25) + 1)
					
		numeros = list(set(numeros))
		numeros_comuns = intersecao(proximo.numeros, numeros, True) 
		return numeros_comuns >= minimo

	@staticmethod
	def verificarSomaSequencialNaoTemNosAnteriores(proximo : Sorteio, anteriores : list[Sorteio], somas = [0,0,0], minimo = 15):
		valido = True
		numeros = []
		for i in range(15):
			soma = 0
			for (p, v) in enumerate(somas):
				soma += anteriores[p].numeros[i] + v

			numeros.append((abs(soma) % 25) + 1)
			
		numeros = list(set(numeros))
		numeros_comuns = intersecao(proximo.numeros, numeros, True) 
		valido = valido and numeros_comuns >= minimo
		
		
		return not valido
	
	@staticmethod	
	def verificarMediaNumerosPosicao(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1]):
				
		numeros = []
		for p in posicoes:
			temps = []
			for a in anteriores:
				temps.append(a.numeros[p])
				
			media = int(mediaNumeros(temps))
			numeros.append(media)

		numeros = list(set(numeros))

			
		valido = intersecao(proximo.numeros, numeros, True) == len(numeros)
		
		return valido
	
	@staticmethod
	def verificarMediaNumerosPosicaoMinimo(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1], minimo = 2, inverter = False):
	
		numeros = []
		for p in posicoes:
			temps = []
			for a in anteriores:
				temps.append(a.numeros[p])

			media = int(mediaNumeros(temps))
			numeros.append(media)

		numeros = list(set(numeros))
			
		valido = intersecao(proximo.numeros, numeros, True) >= minimo
		
		
		return valido if inverter else not valido
	

	@staticmethod
	def verificarSomasProximaPosicao(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1,2,3,4,5,6,7,8,9,10,11], somas = [2,0,1,0,1,-2,-1,-3,-2,1,0,0]):

		numeros = []
		for (i, p) in enumerate(posicoes):
			numeros.append(anteriores[0].numeros[p] + somas[i])

		numeros = list(set(numeros))

			
		valido = intersecao(pegarPosicoes(proximo.numeros, [x+1 for x in posicoes]), numeros, True) == len(numeros)
		
		return valido


	@staticmethod
	def verificarSomasProximaPosicaoV2(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0,1,2,3,4,5,6,7,8,9,10,11], somas = [2,0,1,0,1,-2,-1,-3,-2,1,0,0]):
	
		numeros = []
		for (i, p) in enumerate(posicoes):
			numeros.append(anteriores[0].numeros[p] + somas[i])

		numeros = list(set(numeros))

			
		valido = intersecao(pegarPosicoes(proximo.numeros, [x+1 for x in posicoes]), numeros, True) == 1
		
		return valido
	
	@staticmethod
	def verificarMediaDiferentesNoProximo(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [1]):
		
		numeros = []
		for (i, p) in enumerate(posicoes):
			temp = []
			for a in anteriores:
				temp.append(a.numeros[p])

			numeros.append(mediaNumeros(temp))
		
		numeros = list(set(numeros))

		valido = intersecao(proximo.numeros, numeros, True) > 0
		
		return not valido
	
	@staticmethod
	def verificarMediaDiferentesNoProximoV2(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [1]):
		numeros = []
		for (i, p) in enumerate(posicoes):
			temp = []
			for a in anteriores:
				temp.append(a.numeros[p])

			temp = list(set(temp))
			numeros.append(mediaNumeros(temp))
		
		numeros = list(set(numeros))

		valido = intersecao(proximo.numeros, numeros, True) > 0

		
		return not valido
	
	@staticmethod
	def verificarMediaSerUmaDasPosicoes(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [1], posicoes2 = [0]):
		numeros = []
		for a in anteriores:
			media = mediaNumeros(pegarPosicoes(a.numeros, posicoes))
			numeros.append(media)
			media = mediaNumeros(pegarPosicoes(a.numeros, posicoes2))
			numeros.append(media)

		media = mediaNumeros(pegarPosicoes(proximo.numeros, posicoes))
		numeros.append(media)
		media = mediaNumeros(pegarPosicoes(proximo.numeros, posicoes2))
		numeros.append(media)

		numeros = list(set(numeros))

		valido = intersecao(proximo.numeros, numeros, True) > 0

		
		return not valido
	
	@staticmethod
	def verificarChaveContinuaIntervalo(proximo : Sorteio, anteriores : list[Sorteio], intervalo = 2):				
		chaves = []
		chaves_proximo = []
		for n in range(0, 16-intervalo):
			chaves_proximo.append(chavePosicoes(proximo.numeros, range(n, n+intervalo)))
			for a in anteriores:
				chaves.append(chavePosicoes(a.numeros, range(n, n+intervalo)))

		chaves = list(set(chaves))
		valido = intersecao(chaves_proximo, chaves, True) > 4
		return valido
	
	@staticmethod
	def verificarChaveContinuaIntervaloV2(proximo : Sorteio, anteriores : list[Sorteio], intervalo = 2):				
		chaves = []
		chaves_proximo = []
		for n in range(0, 16-intervalo):
			chaves_proximo.append(chavePosicoes(proximo.numeros, range(n, n+intervalo)))
			for a in anteriores:
				chaves.append(chavePosicoes(a.numeros, range(n, n+intervalo)))

		chaves = list(set(chaves))
		valido = intersecao(chaves_proximo, chaves, True) > 4
		return not valido

	@staticmethod
	def verificarPosicaoSomaValores(proximo : Sorteio, posicoes = [0], somas = [1,1,2]):
		valido = False
		for n in posicoes:
			n_proximo = proximo.numeros[n]
			numeros = [n_proximo + p for p in somas]
			valido = valido or intersecao(proximo.numeros, numeros, True) == 2# len(numeros)
	
		return not valido
	
	@staticmethod
	def verificarPosicaoSomaValoresV2(proximo : Sorteio, posicoes = [0], somas = [1,1,2]):
		valido = True
		for n in posicoes:
			n_proximo = proximo.numeros[n]
			numeros = [n_proximo + p for p in somas]
			valido = valido and intersecao(proximo.numeros, numeros, True) == len(numeros)
	
		return valido
	
	@staticmethod
	def verificarChaveDiferencaAnterior(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [0]):
		diferencas_ant = []
		diferencas_prox = []
		for n in posicoes:
			diferencas_ant.append(anteriores[0].numeros[n] - anteriores[-1].numeros[n])
			diferencas_prox.append(anteriores[-1].numeros[n] - proximo.numeros[n])
	
		
		return chaveNumeros(diferencas_prox) == chaveNumeros(diferencas_ant)