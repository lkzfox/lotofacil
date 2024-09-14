import pprint
from libs.helper import obterTodasSequencias, somaPosicoes

class Sorteio():
	concurso: int = ''
	numeros: list[int]
	
	def __init__(self, estrutura: dict):
		for (chave, valor) in estrutura.items():
			setattr(self, chave, valor)

	def setSequencias(self, tamanho = 3):
		self.sequencias = obterTodasSequencias(self.numeros, tamanho)

	def setSomaPosicoesPares(self):
		self.soma_posicoes_pares = somaPosicoes(self.numeros, range(0, 16, 2))

	def setSomaPosicoesImpares(self):
		self.soma_posicoes_impares = somaPosicoes(self.numeros, range(1, 15, 2))

	def setChaveIntervalo(self, intervalo = 5):
		quantidades = []
		for n in range(1, 26, intervalo):
			quantidades.append(str(len([x for x in self.numeros if x in range(n, n+intervalo)])))
		
		setattr(self, 'chave_intervalo_'+str(intervalo), '.'.join(quantidades))
		
	def getChaveIntervalo(self, intervalo = 5):
		return getattr(self, 'chave_intervalo_'+str(intervalo))
	
	def print(self):
		pprint.pp(self.__class__)
		pprint.pp(self.__dict__)

