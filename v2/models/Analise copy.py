import pprint
import random
import time
from itertools import combinations
from libs.helper import obterTodasSequencias, intersecao, somaPosicoes, chavePosicoes, maxDiferencaVizinhos, maxSequencia, chaveNumeros, resolver, pegarPosicoes, numerosChave, buscarCombos, ranquearOcorrencias, mediaNumeros, fatorarAnteriores, multiplicarPosicoes, numerosPares
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
			'Acerto': acerto
		}
		if qtd_igual < 25: None
		pprint.pp(caracteristicas)
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
				# break
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
	def verificarNaoAcontecimentosPorNumeros(self, numeros = [0], retornando = False):
		_sorteios = list(filter(lambda x : intersecao(x.numeros, numeros, True) == len(numeros), self.sorteios))
		idx_sorteios, tamanho_procurado = 0, 9
		inicio = time.time()
		retorno = {**self._getCombinacoes(tamanho_procurado)}
		for sorteio in self.sorteios:
			if idx_sorteios >= len(_sorteios): continue
			if (sorteio.concurso - 1) != _sorteios[idx_sorteios].concurso: continue
						
			for c in combinations(sorteio.numeros, tamanho_procurado):
				chave = chaveNumeros(c)
				retorno[chave] = retorno[chave] + 1
					
			idx_sorteios += 1


		valido = False
		lista_nao_sairam = []
		for c, va in retorno.items():
			if va > 0: continue
			not retornando and print(c, va)
			valido = True
			lista_nao_sairam.append(numerosChave(c))

		if retornando:
			print(time.time() - inicio)
			return random.choices(lista_nao_sairam, k=250)
			
		valido and pprint.pp({
			'Jogos Analisados': len(_sorteios),
			'Primeiro': _sorteios[0].concurso
		})

	def _getCombinacoes(self, tamanho = 7):
		if len(self.combinacoes.keys()) > 0:
			print('zerando')
			# for c, v in self.combinacoes.items():
			# 	self.combinacoes[c] = 0
		else:
			print('gerando')
			for c in combinations(range(1, 26), tamanho):
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
			if ValidacaoAnalise.compararOcorrenciaRank(proximo, anteriores, posicoes, rank, tamanho):
				self.setInvalido(proximo)
				qtd_igual += 1

		acerto =  round(1 - qtd_igual / jogos_analisados, 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		qtd_igual < 1 and print(retorno, posicoes)

	
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
	def compararOperacaoPosicoes(self, posicoes : list = [], operandos = ['-'], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			jogos_analisados += 1
			anterior, proximo = _sorteios[idx-1], _sorteios[idx]
			self.setValido(proximo)
			
			if ValidacaoAnalise.compararOperacaoPosicoes(proximo, anterior, posicoes, operandos):
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
	def compararFatoracaoSorteiosAnteriores(self, qtd_iteracoes = 5, tamanaho_lista = 6):
		_sorteios = self.sorteios[-tamanaho_lista:]
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
					print('---- TEM IGUAL ----', i)
				else:
					chave_ant[str(i)] = posicoes
				print(posicoes, i, pegarPosicoes(ant.numeros, posicoes))
				montado.append(posicoes)

		analitico['ger']['iteracoes'] = iteracoes
		analitico['ger']['iteracoes_maxima'] = iteracoes * qtd_iteracoes
		pprint.pp(analitico)

	## Descrição - Verificar se em uma certa posição o numero é composto por uma combinaão de outros numeros do mesmo sorteio
	# 1. Buscar a posição específica
	# 2. Verificar se existe uma combinaçaõd e X dígitos que geram o numero na posição
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

	## Descrição - Comparar se chave gerada pelas caracteristicas dos números do proximo sorteio ser igual a mesma chava do sorteio anterior
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
		qtd_igual < 1 and pprint.pp(retorno)

	## Descrição - Comparar se uma função executada sobre o sorteio anterior gera um numero presente no sorteio seguinte
	# 1. Buscar o resutlado da fução aplicada no sorteio anterior
	# 2. Verificar se esse resultado está presente no sorteio seguinte
	# 3. Garantir que só seja executado para resultados entre 1 e 25
	def compararOperacaoPosicoesContem(self, posicoes = [], operacoes = [], retornando = False):
		_sorteios = self.sorteios
		jogos_analisados, qtd_igual = 0, 0
		for idx in range(1, len(_sorteios)):
			anterior, proximo = _sorteios[idx - 1], _sorteios[idx]
			self.setValido(proximo)

			valor_anterior = resolver(posicoes, operacoes, anterior.numeros)
			if valor_anterior in range(1,26):
				jogos_analisados += 1
			if valor_anterior in proximo.numeros:
				self.setInvalido(proximo)
				qtd_igual += 1

				# if qtd_igual > 3: break
		
		acerto =  round(1 - qtd_igual / max(jogos_analisados, 1), 2)
		retorno = {
			'Jogos Analisados': jogos_analisados,
			'Qtd Igual': qtd_igual,
			'Acerto': acerto
		}
		if retornando: return retorno
		if jogos_analisados == (len(_sorteios) - 1):
			print(posicoes, operacoes)
			pprint.pp(retorno)


	## Descrição - Verificar o intervalo alacançado ao aplicar uma função nas posições
	# 1. Gerar o valor da operação nos sorteios
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


##############################################################################################################################################################################
#                                                                                                                                                                            #
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                                                            #
##############################################################################################################################################################################

class ValidacaoAnalise():
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
	def compararOcorrenciaRank(proximo : Sorteio, anteriores : list[Sorteio], posicoes = [], rank = None, tamanho = 10):
		if not rank: rank = ranquearOcorrencias(anteriores)
		posicoes_rank = pegarPosicoes(rank, posicoes)
		contem = intersecao(posicoes_rank, proximo.numeros, True) == len(posicoes_rank)
		return contem
	
	@staticmethod
	def compararOperacaoPosicoes(proximo : Sorteio, anterior : Sorteio, posicoes : list = [], operandos = ['-']):
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
	def verificarCaracteristicasPosicaoV2(proximo : Sorteio, anterior : Sorteio, posicoes = [0], posicoes_chave = [], modo = ''):
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
	def fun01(proximo : Sorteio, posicoes = [0], operacoes = [], lista = []):
		num_prox = resolver(posicoes, operacoes, proximo.numeros)
		return num_prox not in lista