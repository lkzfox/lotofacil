from libs.file_manager import lerSorteados
from libs.data_process import gerarSorteioSimples
from models.Analise import Analise, ValidacaoAnalise
from itertools import combinations
import pprint
import random

class Gerador:
	sorteios = []
	regras = []

	def __init__(self):
		self.sorteios = lerSorteados()

	def limparRegras(self):
		self.regras = []

	def addRegra(self, funcao, **kwargs):
		self.regras.append({ 'fn': funcao, 'args': kwargs, 'inverter': False })

	def addRegraSemArgs(self, funcao, **kwargs):
		self.regras.append({ 'fn': funcao, 'args': kwargs, 'inverter': False, 'sem_args': True })

	def addRegraInvertida(self, funcao, **kwargs):
		self.regras.append({ 'fn': funcao, 'args': kwargs, 'inverter': True })

	def buscarNumeros(self, qtd_possibilidades = 1000):
		possiveis = list(combinations(range(1, 26), 15))
		qtd_buscada, qtd_valida = 0, 0
		tamanho_real = len(possiveis)
		while True:
			qtd_buscada += 1
			print(len(possiveis), ' - ', qtd_buscada, ' - ', qtd_valida, ' => ', qtd_valida * 100 / qtd_buscada, end='\r')
			index = random.randrange(0, len(possiveis))
			proximo = gerarSorteioSimples(possiveis[index])
			possiveis.pop(index)
			for r in self.regras:
				metodo = r['fn'].__name__ if type(r['fn']).__name__ in ['method', 'function'] else r['fn']				
				invalido = getattr(ValidacaoAnalise, metodo)(**r['args'], proximo=proximo)
				if invalido: 
				# 	print('Regra Falhou:', metodo, 'Args:', r['args'])
				# 	print('Buscados:', qtd_buscada)
				# 	print(proximo.numeros, invalido)
					break
				# 	exit()

			if not invalido: 
				print(proximo.numeros)
				qtd_valida += 1

			if qtd_valida == qtd_possibilidades:
				print(len(possiveis), ' - ', qtd_buscada, ' - ', qtd_valida, ' => ', qtd_valida * 100 / qtd_buscada, end='\r')
				break

	def calcularReducao(self, maximo_analises = 4000000):
		possiveis = list(combinations(range(1, 26), 15))
		qtd_buscada, qtd_valida = 0, 0
		print('Total de Regras:', len(self.regras))
		while True:
			qtd_buscada += 1
			print(len(possiveis), ' - ', qtd_buscada, ' - ', qtd_valida, ' - ', qtd_buscada - qtd_valida - 1, ' => ', qtd_valida * 100 / qtd_buscada, end='\r')
			index = random.randrange(0, len(possiveis))
			proximo = gerarSorteioSimples(possiveis[index])
			possiveis.pop(index)
			for r in self.regras:
				metodo = r['fn'].__name__ if type(r['fn']).__name__ in ['method', 'function'] else r['fn']				
				invalido = getattr(ValidacaoAnalise, metodo)(**r['args'], proximo=proximo)
				if invalido: 
					break

			if not invalido: 
				qtd_valida += 1

			if len(possiveis) == 0 or qtd_buscada == maximo_analises:
				break
		
		print(len(possiveis), ' - ', qtd_buscada, ' - ', qtd_valida, ' - ', qtd_buscada - qtd_valida - 1, ' => ', qtd_valida * 100 / qtd_buscada)


	def buscarNumerosTeste(self):
		possiveis = list(combinations(range(1, 26), 15))
		qtd_buscada, qtd_valida = 0, 0
		while True:
			if not len(possiveis): break
			qtd_buscada += 1
			index = random.randrange(0, len(possiveis))
			proximo = gerarSorteioSimples(possiveis[index])
			possiveis.pop(index)
			for r in self.regras:
				metodo = r['fn'].__name__ if type(r['fn']).__name__ in ['method', 'function'] else r['fn']				
				invalido = getattr(ValidacaoAnalise, metodo)(**r['args'], proximo=proximo)
				if invalido: 
					prt_arg = not r.get('sem_args')
					print('Regra Falhou:', metodo, 'Args:', r['args'] if prt_arg else '')
					print('Buscados:', qtd_buscada)
					print(proximo.numeros, invalido)
					exit()
					break

			if not invalido: 
				qtd_valida += 1		
				print(proximo.numeros, ' -> ', qtd_buscada, 'Válidos: ' + str(qtd_valida))

		print(proximo.numeros, ' -> ', qtd_buscada, qtd_valida)

	def analisarSorteio(self, sorteio = [0,0,0,0]):
		proximo = gerarSorteioSimples(sorteio)
		conjunto_invalido = False
		for r in self.regras:
			metodo = r['fn'].__name__ if type(r['fn']).__name__ in ['method', 'function'] else r['fn']				
			invalido = getattr(ValidacaoAnalise, metodo)(**r['args'], proximo=proximo)
			if invalido: 
				conjunto_invalido = True
				prt_arg = not r.get('sem_args')
				print('Regra Falhou:', metodo, 'Args:', r['args'] if prt_arg else '')

		print(' -------- Finalizado -------- ')
		return conjunto_invalido