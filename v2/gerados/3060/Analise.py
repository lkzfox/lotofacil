import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from models.Analise import *
from libs.file_manager import lerSorteados

sorteios = lerSorteados()[-1500:]
analise = Analise(sorteios)

# # analise.sequenciaRepetidaJogoAnterior(50, 4)
# analise.compararSomaPosicoesPares()
# analise.compararSomaPosicoesImpares()

# posicoes = [[1, 3, 6, 9] , [1, 3, 7, 12] , [2, 7, 11, 12] , [3, 5, 7, 12] , [3, 5, 9, 12] , [3, 5, 9, 13] , [3, 5, 10, 12] , [3, 5, 10, 13] , [3, 6, 7, 12] , [3, 6, 9, 12] , [3, 6, 10, 12] , [3, 6, 10, 13] , [3, 7, 8, 12] , [3, 7, 10, 12] , [3, 7, 10, 13] , [3, 7, 10, 14] , [3, 8, 10, 13], [3, 6, 12], [4,9], [4,10], [1, 3, 5, 6, 10], [1, 3, 5, 7, 10], [1, 3, 5, 9, 14], [1, 3, 5, 10, 14], [1, 3, 7, 8, 14], [1, 3, 7, 9, 14], [1, 5, 6, 10, 11], [1, 5, 7, 10, 11], [1, 5, 9, 10, 11], [1, 5, 9, 11, 14], [1, 5, 10, 11, 14], [2, 3, 5, 7, 10], [2, 3, 7, 8, 14], [2, 4, 7, 8, 11], [2, 5, 7, 10, 11], [2, 5, 9, 11, 12], [2, 6, 8, 11, 12], [2, 6, 9, 11, 12], [2, 7, 9, 11, 14], [2, 8, 9, 11, 12], [3, 6, 9, 13, 14], [3, 7, 11, 12, 14], [3, 8, 9, 11, 12], [3, 8, 9, 13, 14], [6, 7, 10, 11, 13], [6, 8, 10, 11, 12], [6, 8, 10, 11, 13]]
# for p in posicoes:
# 	analise.compararChavePosicoes(p)

# posicoes = [[0, 4, 6, 7, 8],[1, 2, 5, 8, 13]] #[0, 8, 10, 13], ,  [0, 6, 8, 10]
# for p in posicoes:
# 	analise.compararChavePosicoesComAnterior(p)

# analise.compararSomas()

# analise.compararMultiplicacoes()

# caracteristicas = [('soma_pares', 'soma_impares'), ('soma_pares', 'soma_primos'), ('soma_pares', 'soma_menores_13'), ('soma_impares', 'soma_menores_10'), ('soma_impares', 'soma_entre_10_20'), ('soma_impares', 'soma_maiores_20'), ('soma_impares', 'soma_menores_13'), ('soma_impares', 'soma_maiores_13'), ('soma_impares', 'soma_meio'), ('soma_impares', 'soma_col_2'), ('soma_impares', 'soma_col_3'), ('soma_menores_10', 'soma_primos'), ('soma_menores_10', 'soma_maiores_13'), ('soma_entre_10_20', 'soma_menores_13'), ('soma_entre_10_20', 'soma_col_1'), ('soma_entre_10_20', 'soma_col_2'), ('soma_maiores_20', 'soma_primos'), ('soma_primos', 'soma_menores_13'), ('soma_primos', 'soma_maiores_13'), ('soma_primos', 'soma_meio'), ('soma_menores_13', 'soma_maiores_13'), ('soma_menores_13', 'soma_meio'), ('soma_maiores_13', 'soma_col_1'), ('soma_maiores_13', 'soma_col_3'), ('soma_maiores_13', 'soma_col_4'), ('soma_meio', 'soma_col_3')]
# for c in caracteristicas:
# 	analise.compararCaracteristicas(c)


# analise.verificarPossibilidadePosicao(0)
# analise.verificarPossibilidadePosicao(1)
# analise.verificarPossibilidadePosicao(2)
# analise.verificarPossibilidadePosicao(3)
# analise.verificarPossibilidadePosicao(4)
# analise.verificarPossibilidadePosicao(5)
# analise.verificarPossibilidadePosicao(6)
# analise.verificarPossibilidadePosicao(7)
# analise.verificarPossibilidadePosicao(8)
# analise.verificarPossibilidadePosicao(9)
# analise.verificarPossibilidadePosicao(10)
# analise.verificarPossibilidadePosicao(11)
# analise.verificarPossibilidadePosicao(12)
# analise.verificarPossibilidadePosicao(13)
# analise.verificarPossibilidadePosicao(14)

# analise.contarQuantidadeRepetida()

# analise.verificarMaximaDiferencaVizinhos()

# analise.verificarTamanhoMaximoSequencia()


# analise.verificarCaracteristica('pares')
# analise.verificarCaracteristica('quantidade_primos')
# analise.verificarCaracteristica('quantidade_menores_10')
# analise.verificarCaracteristica('quantidade_entre_10_20')
# analise.verificarCaracteristica('quantidade_maiores_20')
# analise.verificarCaracteristica('quantidade_meio')
# analise.verificarCaracteristica('quantidade_menores_13')

# analise.verificarCaracteristica('quantidade_col_1')
# analise.verificarCaracteristica('quantidade_col_2')
# analise.verificarCaracteristica('quantidade_col_3')
# analise.verificarCaracteristica('quantidade_col_4')
# analise.verificarCaracteristica('quantidade_col_5')

# analise.compararChavesIntervalos(distancia = 1, intervalo = 2)
# analise.compararChavesIntervalos(distancia = 1, intervalo = 3)


# analise.compararChavesIntervalos(distancia = 1, intervalo = 2)
# analise.compararChavesIntervalos(distancia = 1, intervalo = 3)
# analise.compararChavesIntervalos(distancia = 2, intervalo = 4)
# analise.compararChavesIntervalos(distancia = 4, intervalo = 4)
# analise.compararChavesIntervalos(distancia = 8, intervalo = 4)
# analise.compararChavesIntervalos(distancia = 9, intervalo = 4)
# analise.compararChavesIntervalos(distancia = 16, intervalo = 6)


# for n in range(1, 12):
# 	analise.compararDiferencaPosicaoSimples(n)

# for n in range(1, 11):
# 	analise.compararSomaPosicaoSimples(n)


# analise.compararOperacoesPosicoes(posicoes = (0, 3, 4, 8, 11, 13, 14), operacoes = ('-', '-', '-', '*', '+', '+'))
# analise.compararOperacoesPosicoes(posicoes = (0, 3, 5, 6, 7, 8, 12), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (0, 4, 6, 8, 9, 11, 13), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (0, 4, 7, 8, 9, 11, 12), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (0, 5, 6, 7, 9, 11, 12), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (0, 5, 6, 7, 10, 11, 12), operacoes = ('-', '-', '*', '-', '+', '+'))
# analise.compararOperacoesPosicoes(posicoes = (1, 2, 6, 8, 9, 11, 12), operacoes = ('-', '+', '+', '*', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (1, 3, 5, 6, 8, 9, 12), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (1, 4, 5, 6, 8, 9, 11), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (1, 4, 5, 7, 9, 11, 13), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (1, 4, 5, 8, 9, 11, 13), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (2, 3, 4, 5, 7, 9, 11), operacoes = ('-', '-', '-', '*', '+', '+'))
# analise.compararOperacoesPosicoes(posicoes = (2, 3, 5, 7, 9, 10, 13), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (2, 5, 6, 8, 9, 11, 12), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (3, 4, 7, 9, 11, 12, 14), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (3, 5, 6, 7, 8, 12, 14), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (3, 5, 6, 7, 9, 11, 12), operacoes = ('+', '*', '-', '+', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (3, 5, 6, 8, 10, 11, 13), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (3, 5, 6, 9, 11, 13, 14), operacoes = ('-', '-', '-', '*', '+', '+'))
# analise.compararOperacoesPosicoes(posicoes = (3, 5, 7, 9, 10, 12, 14), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (3, 6, 7, 9, 10, 13, 14), operacoes = ('+', '+', '*', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (3, 7, 8, 9, 11, 13, 14), operacoes = ('+', '*', '+', '-', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (4, 5, 7, 8, 9, 11, 12), operacoes = ('-', '+', '+', '*', '-', '-'))
# analise.compararOperacoesPosicoes(posicoes = (4, 5, 7, 9, 11, 12, 14), operacoes = ('+', '*', '-', '-', '-', '+'))
	
# lista = [(0, 3, 6), (0, 3, 6, 8, 11, 13),(0, 3, 6, 9, 11, 13),(0, 4, 6, 8, 11, 13),(1, 2, 6, 8, 11, 13),(1, 2, 6, 9, 11, 13),(1, 3, 4, 7, 10, 12),(1, 3, 6, 7, 9, 14),(1, 3, 6, 9, 11, 13)]
# for idx, n in enumerate(lista):
# 	print(idx, end='\r')
# 	analise.verificarRepeticaoChave(n, True)


# lista = [['pares', (0, 3, 6, 8)],['pares', (0, 3, 6, 9)],['pares', (0, 3, 12, 14)],['pares', (1, 3, 6, 9)],['pares', (1, 3, 9, 14)],['pares', (1, 3, 10, 12)],['pares', (1, 3, 10, 13)],['pares', (1, 4, 10, 11)],['pares', (1, 5, 10, 11)],['pares', (1, 7, 10, 11)],['pares', (2, 3, 9, 11)],['pares', (2, 3, 9, 13)],['pares', (2, 3, 9, 14)],['pares', (2, 3, 10, 13)],['pares', (2, 4, 8, 11)],['pares', (2, 4, 9, 11)],['pares', (2, 4, 10, 11)],['pares', (2, 5, 8, 11)],['pares', (2, 5, 9, 11)],['pares', (2, 5, 10, 11)],['pares', (2, 6, 8, 11)],['pares', (2, 7, 8, 11)],['pares', (2, 7, 9, 11)],['pares', (2, 7, 10, 11)],['pares', (2, 7, 11, 12)],['pares', (2, 8, 9, 11)],['pares', (2, 8, 10, 11)],['pares', (2, 8, 11, 12)],['pares', (3, 4, 10, 13)],['pares', (3, 5, 6, 10)],['pares', (3, 5, 7, 10)],['pares', (3, 5, 8, 10)],['pares', (3, 5, 8, 14)],['pares', (3, 5, 9, 14)],['pares', (3, 5, 10, 14)],['pares', (3, 6, 8, 10)],['pares', (3, 6, 9, 13)],['pares', (3, 6, 9, 14)],['pares', (3, 6, 10, 13)],['pares', (3, 6, 10, 14)],['pares', (3, 7, 8, 10)],['pares', (3, 7, 9, 10)],['pares', (3, 7, 9, 14)],['pares', (3, 7, 10, 11)],['pares', (3, 7, 10, 12)],['pares', (3, 7, 10, 13)],['pares', (3, 7, 10, 14)],['pares', (3, 8, 9, 14)],['pares', (3, 8, 10, 13)],['pares', (3, 8, 10, 14)],['pares', (3, 9, 10, 13)],['pares', (3, 9, 10, 14)],['pares', (3, 9, 11, 14)],['pares', (3, 9, 12, 14)],['pares', (3, 9, 13, 14)],['pares', (3, 10, 11, 13)],['pares', (3, 10, 13, 14)],['pares', (5, 10, 11, 13)],['impares', (0, 3, 6, 8)],['impares', (0, 3, 6, 9)],['impares', (0, 3, 12, 14)],['impares', (1, 3, 6, 9)],['impares', (1, 3, 9, 14)],['impares', (1, 3, 10, 12)],['impares', (1, 3, 10, 13)],['impares', (1, 4, 10, 11)],['impares', (1, 5, 10, 11)],['impares', (1, 7, 10, 11)],['impares', (2, 3, 9, 11)],['impares', (2, 3, 9, 13)],['impares', (2, 3, 9, 14)],['impares', (2, 3, 10, 13)],['impares', (2, 4, 8, 11)],['impares', (2, 4, 9, 11)],['impares', (2, 4, 10, 11)],['impares', (2, 5, 8, 11)],['impares', (2, 5, 9, 11)],['impares', (2, 5, 10, 11)],['impares', (2, 6, 8, 11)],['impares', (2, 7, 8, 11)],['impares', (2, 7, 9, 11)],['impares', (2, 7, 10, 11)],['impares', (2, 7, 11, 12)],['impares', (2, 8, 9, 11)],['impares', (2, 8, 10, 11)],['impares', (2, 8, 11, 12)],['impares', (3, 4, 10, 13)],['impares', (3, 5, 6, 10)],['impares', (3, 5, 7, 10)],['impares', (3, 5, 8, 10)],['impares', (3, 5, 8, 14)],['impares', (3, 5, 9, 14)],['impares', (3, 5, 10, 14)],['impares', (3, 6, 8, 10)],['impares', (3, 6, 9, 13)],['impares', (3, 6, 9, 14)],['impares', (3, 6, 10, 13)],['impares', (3, 6, 10, 14)],['impares', (3, 7, 8, 10)],['impares', (3, 7, 9, 10)],['impares', (3, 7, 9, 14)],['impares', (3, 7, 10, 11)],['impares', (3, 7, 10, 12)],['impares', (3, 7, 10, 13)],['impares', (3, 7, 10, 14)],['impares', (3, 8, 9, 14)],['impares', (3, 8, 10, 13)],['impares', (3, 8, 10, 14)],['impares', (3, 9, 10, 13)],['impares', (3, 9, 10, 14)],['impares', (3, 9, 11, 14)],['impares', (3, 9, 12, 14)],['impares', (3, 9, 13, 14)],['impares', (3, 10, 11, 13)],['impares', (3, 10, 13, 14)],['impares', (5, 10, 11, 13)],['maior_sequencia', (0, 2, 8, 12)],['maior_sequencia', (0, 3, 6, 9)],['maior_sequencia', (0, 3, 8, 10)],['maior_sequencia', (0, 4, 8, 11)],['maior_sequencia', (0, 6, 8, 11)],['maior_sequencia', (0, 6, 8, 12)],['maior_sequencia', (1, 3, 6, 9)],['maior_sequencia', (1, 3, 7, 12)],['maior_sequencia', (1, 3, 8, 10)],['maior_sequencia', (1, 4, 5, 9)],['maior_sequencia', (1, 4, 5, 10)],['maior_sequencia', (1, 4, 6, 9)],['maior_sequencia', (1, 4, 6, 12)],['maior_sequencia', (1, 4, 7, 9)],['maior_sequencia', (1, 4, 7, 12)],['maior_sequencia', (1, 4, 8, 10)],['maior_sequencia', (1, 4, 9, 11)],['maior_sequencia', (1, 4, 9, 13)],['maior_sequencia', (1, 5, 6, 9)],['maior_sequencia', (1, 5, 6, 10)],['maior_sequencia', (1, 5, 7, 12)],['maior_sequencia', (1, 5, 9, 12)],['maior_sequencia', (1, 5, 10, 11)],['maior_sequencia', (1, 5, 10, 12)],['maior_sequencia', (1, 6, 7, 12)],['maior_sequencia', (1, 6, 8, 12)],['maior_sequencia', (1, 7, 8, 12)],['maior_sequencia', (1, 7, 9, 12)],['maior_sequencia', (1, 7, 10, 12)],['maior_sequencia', (1, 7, 11, 12)],['maior_sequencia', (1, 8, 10, 12)],['maior_sequencia', (2, 3, 7, 10)],['maior_sequencia', (2, 3, 8, 10)],['maior_sequencia', (2, 4, 6, 12)],['maior_sequencia', (2, 4, 6, 13)],['maior_sequencia', (2, 4, 7, 10)],['maior_sequencia', (2, 4, 7, 12)],['maior_sequencia', (2, 4, 8, 10)],['maior_sequencia', (2, 4, 9, 13)],['maior_sequencia', (2, 4, 10, 13)],['maior_sequencia', (2, 5, 7, 12)],['maior_sequencia', (2, 7, 10, 12)],['maior_sequencia', (2, 7, 11, 12)],['maior_sequencia', (2, 7, 11, 14)],['maior_sequencia', (2, 8, 10, 12)],['maior_sequencia', (3, 4, 6, 12)],['maior_sequencia', (3, 4, 8, 13)],['maior_sequencia', (3, 4, 9, 13)],['maior_sequencia', (3, 5, 8, 12)],['maior_sequencia', (3, 5, 9, 12)],['maior_sequencia', (3, 5, 10, 12)],['maior_sequencia', (3, 5, 10, 13)],['maior_sequencia', (3, 6, 7, 12)],['maior_sequencia', (3, 6, 8, 12)],['maior_sequencia', (3, 6, 9, 12)],['maior_sequencia', (3, 6, 10, 12)],['maior_sequencia', (3, 6, 12, 14)],['maior_sequencia', (3, 7, 8, 12)],['maior_sequencia', (3, 7, 10, 12)],['maior_sequencia', (4, 6, 7, 12)],['maior_sequencia', (4, 6, 8, 12)],['maior_sequencia', (4, 6, 8, 13)],['maior_sequencia', (4, 7, 8, 12)],['maior_sequencia', (4, 7, 9, 12)],['maior_sequencia', (4, 7, 9, 13)],['maior_sequencia', (4, 7, 11, 12)],['maior_sequencia', (5, 6, 7, 12)],['maior_sequencia', (5, 6, 8, 12)],['maior_sequencia', (5, 7, 8, 12)],['maior_sequencia', (5, 7, 9, 12)],['maior_sequencia', (6, 7, 10, 12)],['maior_sequencia', (6, 8, 10, 12)],['maior_sequencia', (6, 8, 11, 12)],['maior_sequencia', (6, 8, 12, 13)],['quantidade_sequencias', (1, 3, 7, 9)],['quantidade_sequencias', (1, 3, 7, 12)],['quantidade_sequencias', (1, 4, 7, 9)],['quantidade_sequencias', (1, 4, 7, 12)],['quantidade_sequencias', (1, 4, 9, 11)],['quantidade_sequencias', (2, 4, 7, 11)],['quantidade_sequencias', (2, 4, 7, 12)],['quantidade_sequencias', (2, 5, 7, 11)],['quantidade_sequencias', (2, 5, 7, 12)],['quantidade_sequencias', (2, 5, 9, 12)],['quantidade_sequencias', (2, 6, 10, 13)],['quantidade_sequencias', (2, 7, 10, 12)],['quantidade_sequencias', (2, 7, 11, 12)],['quantidade_sequencias', (3, 5, 7, 11)],['quantidade_sequencias', (3, 5, 9, 12)],['quantidade_sequencias', (3, 7, 10, 12)],['quantidade_sequencias', (4, 6, 7, 12)],['quantidade_sequencias', (4, 6, 8, 12)],['quantidade_sequencias', (4, 7, 9, 11)],['quantidade_sequencias', (4, 7, 9, 12)],['quantidade_sequencias', (4, 8, 9, 12)],['quantidade_entre_10_20', (1, 3, 6, 9)],['quantidade_primos', (0, 3, 6, 8)],['quantidade_primos', (0, 3, 6, 9)],['quantidade_primos', (1, 3, 6, 8)],['quantidade_primos', (1, 3, 6, 9)],['quantidade_primos', (2, 3, 7, 12)],['quantidade_primos', (2, 4, 9, 11)],['quantidade_primos', (2, 4, 10, 11)],['quantidade_primos', (2, 6, 10, 11)],['quantidade_primos', (2, 7, 10, 11)],['quantidade_primos', (3, 6, 7, 12)],['quantidade_primos', (3, 6, 8, 12)],['quantidade_primos', (3, 6, 9, 12)],['quantidade_primos', (3, 6, 10, 12)],['quantidade_primos', (3, 7, 10, 12)],['diferenca_maxima', (0, 4, 7, 10)],['diferenca_maxima', (1, 2, 4, 10)],['diferenca_maxima', (1, 4, 5, 9)],['diferenca_maxima', (1, 4, 5, 10)],['diferenca_maxima', (1, 4, 6, 9)],['diferenca_maxima', (1, 4, 6, 10)],['diferenca_maxima', (1, 4, 7, 10)],['diferenca_maxima', (1, 4, 8, 10)],['diferenca_maxima', (1, 4, 9, 10)],['diferenca_maxima', (1, 4, 9, 11)],['diferenca_maxima', (1, 4, 9, 12)],['diferenca_maxima', (1, 4, 9, 13)],['diferenca_maxima', (1, 4, 10, 11)],['diferenca_maxima', (1, 4, 10, 12)],['diferenca_maxima', (1, 4, 10, 13)],['diferenca_maxima', (1, 5, 6, 10)],['diferenca_maxima', (1, 5, 7, 10)],['diferenca_maxima', (1, 5, 10, 11)],['diferenca_maxima', (1, 7, 10, 13)],['diferenca_maxima', (1, 8, 10, 13)],['diferenca_maxima', (2, 4, 7, 10)],['diferenca_maxima', (2, 4, 10, 13)],['diferenca_maxima', (2, 5, 7, 10)],['diferenca_maxima', (2, 6, 10, 13)],['diferenca_maxima', (2, 7, 10, 13)],['diferenca_maxima', (3, 4, 9, 12)],['diferenca_maxima', (3, 4, 10, 13)],['diferenca_maxima', (3, 5, 7, 9)],['diferenca_maxima', (3, 5, 7, 10)],['diferenca_maxima', (3, 6, 10, 13)],['diferenca_maxima', (3, 7, 10, 13)],['diferenca_maxima', (4, 5, 7, 10)],['diferenca_maxima', (4, 6, 7, 10)],['diferenca_maxima', (4, 6, 8, 12)],['diferenca_maxima', (4, 7, 9, 10)],['diferenca_maxima', (4, 7, 9, 11)],['diferenca_maxima', (4, 7, 9, 12)],['diferenca_maxima', (4, 7, 10, 13)],['diferenca_maxima', (4, 8, 9, 12)],['diferenca_maxima', (4, 8, 10, 13)],['diferenca_maxima', (4, 9, 11, 13)],['diferenca_maxima', (5, 7, 10, 12)],['quantidade_menores_13', (1, 3, 5, 10)],['quantidade_menores_13', (1, 4, 9, 11)],['quantidade_menores_13', (3, 4, 8, 12)],['quantidade_menores_13', (3, 5, 8, 12)],['quantidade_menores_13', (3, 5, 11, 12)],['quantidade_menores_13', (3, 8, 10, 13)],['quantidade_maiores_13', (3, 5, 10, 12)],['quantidade_maiores_13', (3, 5, 10, 13)],['quantidade_maiores_13', (3, 8, 10, 13)],['quantidade_meio', (0, 1, 6, 10)],['quantidade_meio', (0, 3, 7, 11)],['quantidade_meio', (0, 4, 7, 10)],['quantidade_meio', (0, 4, 7, 11)],['quantidade_meio', (0, 4, 7, 12)],['quantidade_meio', (0, 4, 7, 13)],['quantidade_meio', (0, 4, 9, 13)],['quantidade_meio', (0, 5, 7, 11)],['quantidade_meio', (1, 3, 6, 9)],['quantidade_meio', (1, 3, 6, 10)],['quantidade_meio', (1, 3, 6, 11)],['quantidade_meio', (1, 3, 7, 9)],['quantidade_meio', (1, 3, 7, 10)],['quantidade_meio', (1, 3, 7, 11)],['quantidade_meio', (1, 3, 7, 12)],['quantidade_meio', (1, 3, 7, 13)],['quantidade_meio', (1, 4, 5, 9)],['quantidade_meio', (1, 4, 6, 9)],['quantidade_meio', (1, 4, 6, 10)],['quantidade_meio', (1, 4, 6, 11)],['quantidade_meio', (1, 4, 7, 9)],['quantidade_meio', (1, 4, 7, 10)],['quantidade_meio', (1, 4, 7, 11)],['quantidade_meio', (1, 4, 7, 12)],['quantidade_meio', (1, 4, 7, 13)],['quantidade_meio', (1, 4, 9, 11)],['quantidade_meio', (1, 4, 9, 13)],['quantidade_meio', (1, 4, 11, 14)],['quantidade_meio', (1, 5, 6, 10)],['quantidade_meio', (1, 5, 7, 10)],['quantidade_meio', (1, 5, 7, 13)],['quantidade_meio', (1, 5, 9, 13)],['quantidade_meio', (1, 6, 7, 13)],['quantidade_meio', (1, 6, 8, 13)],['quantidade_meio', (1, 6, 10, 12)],['quantidade_meio', (1, 6, 10, 13)],['quantidade_meio', (1, 6, 10, 14)],['quantidade_meio', (1, 6, 11, 13)],['quantidade_meio', (1, 7, 9, 13)],['quantidade_meio', (1, 7, 9, 14)],['quantidade_meio', (1, 7, 12, 14)],['quantidade_meio', (2, 4, 7, 10)],['quantidade_meio', (2, 4, 7, 11)],['quantidade_meio', (2, 5, 7, 11)],['quantidade_meio', (2, 6, 11, 12)],['quantidade_meio', (3, 4, 7, 10)],['quantidade_meio', (3, 4, 7, 11)],['quantidade_meio', (3, 5, 7, 11)],['quantidade_meio', (3, 7, 8, 10)],['quantidade_meio', (4, 6, 8, 12)],['quantidade_meio', (4, 7, 9, 10)],['quantidade_meio', (4, 7, 9, 11)],['quantidade_meio', (4, 7, 9, 12)],['quantidade_meio', (4, 7, 10, 13)],['quantidade_meio', (4, 7, 11, 13)],['quantidade_meio', (4, 8, 9, 12)],['quantidade_meio', (4, 9, 10, 13)],['quantidade_meio', (4, 9, 11, 13)],['quantidade_meio', (4, 9, 12, 13)],['quantidade_meio', (5, 7, 11, 13)],['quantidade_col_1', (0, 1, 7, 9)],['quantidade_col_1', (0, 2, 7, 10)],['quantidade_col_1', (1, 3, 7, 9)],['quantidade_col_1', (1, 4, 6, 9)],['quantidade_col_1', (1, 4, 7, 9)],['quantidade_col_1', (1, 4, 9, 11)],['quantidade_col_1', (1, 5, 6, 9)],['quantidade_col_1', (1, 5, 6, 10)],['quantidade_col_1', (1, 5, 7, 9)],['quantidade_col_1', (1, 5, 7, 10)],['quantidade_col_1', (1, 5, 9, 10)],['quantidade_col_1', (1, 5, 9, 11)],['quantidade_col_1', (1, 5, 9, 12)],['quantidade_col_1', (1, 7, 9, 11)],['quantidade_col_1', (1, 7, 9, 13)],['quantidade_col_1', (2, 4, 7, 10)],['quantidade_col_1', (2, 6, 8, 11)],['quantidade_col_1', (2, 7, 8, 11)],['quantidade_col_1', (3, 7, 10, 12)],['quantidade_col_1', (4, 7, 9, 12)],['quantidade_col_1', (4, 9, 11, 13)],['quantidade_col_1', (5, 7, 9, 12)],['quantidade_col_2', (0, 1, 4, 10)],['quantidade_col_2', (0, 2, 4, 10)],['quantidade_col_2', (0, 2, 6, 11)],['quantidade_col_2', (0, 3, 6, 9)],['quantidade_col_2', (0, 3, 6, 10)],['quantidade_col_2', (0, 3, 6, 11)],['quantidade_col_2', (0, 3, 7, 10)],['quantidade_col_2', (0, 4, 6, 9)],['quantidade_col_2', (0, 4, 7, 10)],['quantidade_col_2', (0, 4, 8, 10)],['quantidade_col_2', (0, 4, 9, 10)],['quantidade_col_2', (0, 4, 9, 12)],['quantidade_col_2', (0, 4, 10, 13)],['quantidade_col_2', (1, 2, 6, 9)],['quantidade_col_2', (1, 2, 6, 10)],['quantidade_col_2', (1, 2, 6, 11)],['quantidade_col_2', (1, 3, 6, 9)],['quantidade_col_2', (1, 3, 6, 10)],['quantidade_col_2', (1, 3, 6, 11)],['quantidade_col_2', (1, 3, 7, 10)],['quantidade_col_2', (1, 3, 8, 10)],['quantidade_col_2', (1, 3, 8, 14)],['quantidade_col_2', (1, 4, 5, 10)],['quantidade_col_2', (1, 4, 6, 9)],['quantidade_col_2', (1, 4, 6, 10)],['quantidade_col_2', (1, 4, 6, 11)],['quantidade_col_2', (1, 4, 7, 9)],['quantidade_col_2', (1, 4, 7, 10)],['quantidade_col_2', (1, 4, 8, 10)],['quantidade_col_2', (1, 4, 9, 10)],['quantidade_col_2', (1, 4, 9, 12)],['quantidade_col_2', (1, 4, 10, 12)],['quantidade_col_2', (1, 4, 10, 13)],['quantidade_col_2', (1, 5, 10, 12)],['quantidade_col_2', (1, 6, 8, 10)],['quantidade_col_2', (1, 6, 10, 13)],['quantidade_col_2', (1, 7, 10, 11)],['quantidade_col_2', (1, 7, 10, 12)],['quantidade_col_2', (1, 8, 10, 11)],['quantidade_col_2', (1, 8, 10, 12)],['quantidade_col_2', (2, 4, 7, 10)],['quantidade_col_2', (2, 4, 7, 11)],['quantidade_col_2', (2, 4, 8, 10)],['quantidade_col_2', (2, 4, 8, 12)],['quantidade_col_2', (2, 4, 10, 13)],['quantidade_col_2', (2, 5, 6, 11)],['quantidade_col_2', (2, 6, 8, 12)],['quantidade_col_2', (2, 6, 9, 12)],['quantidade_col_2', (2, 6, 10, 12)],['quantidade_col_2', (2, 6, 11, 12)],['quantidade_col_2', (2, 7, 11, 14)],['quantidade_col_2', (3, 4, 8, 12)],['quantidade_col_2', (3, 4, 10, 13)],['quantidade_col_2', (3, 6, 8, 12)],['quantidade_col_2', (3, 6, 10, 13)],['quantidade_col_2', (3, 7, 10, 12)],['quantidade_col_2', (3, 7, 10, 13)],['quantidade_col_2', (4, 5, 9, 13)],['quantidade_col_2', (4, 6, 8, 12)],['quantidade_col_2', (4, 7, 9, 12)],['quantidade_col_2', (4, 7, 10, 13)],['quantidade_col_2', (4, 8, 9, 12)],['quantidade_col_2', (4, 8, 10, 13)],['quantidade_col_2', (6, 8, 10, 12)],['quantidade_col_3', (0, 3, 4, 8)],['quantidade_col_3', (0, 3, 5, 8)],['quantidade_col_3', (0, 3, 7, 10)],['quantidade_col_3', (0, 3, 8, 11)],['quantidade_col_3', (0, 3, 8, 13)],['quantidade_col_3', (1, 3, 5, 7)],['quantidade_col_3', (1, 3, 5, 8)],['quantidade_col_3', (1, 3, 5, 9)],['quantidade_col_3', (1, 3, 7, 9)],['quantidade_col_3', (1, 3, 7, 10)],['quantidade_col_3', (1, 3, 7, 12)],['quantidade_col_3', (1, 3, 7, 13)],['quantidade_col_3', (1, 3, 7, 14)],['quantidade_col_3', (1, 3, 8, 11)],['quantidade_col_3', (1, 3, 8, 13)],['quantidade_col_3', (1, 4, 6, 11)],['quantidade_col_3', (1, 4, 9, 11)],['quantidade_col_3', (2, 3, 5, 8)],['quantidade_col_3', (2, 3, 5, 9)],['quantidade_col_3', (2, 3, 5, 11)],['quantidade_col_3', (2, 3, 7, 10)],['quantidade_col_3', (2, 4, 7, 11)],['quantidade_col_3', (2, 5, 6, 11)],['quantidade_col_3', (2, 5, 7, 11)],['quantidade_col_3', (2, 6, 11, 12)],['quantidade_col_3', (3, 4, 5, 8)],['quantidade_col_3', (3, 4, 7, 10)],['quantidade_col_3', (3, 4, 7, 12)],['quantidade_col_3', (3, 4, 8, 10)],['quantidade_col_3', (3, 4, 9, 12)],['quantidade_col_3', (3, 4, 10, 12)],['quantidade_col_3', (3, 4, 10, 13)],['quantidade_col_3', (3, 4, 11, 13)],['quantidade_col_3', (3, 5, 6, 8)],['quantidade_col_3', (3, 5, 6, 9)],['quantidade_col_3', (3, 5, 6, 10)],['quantidade_col_3', (3, 5, 6, 11)],['quantidade_col_3', (3, 5, 7, 8)],['quantidade_col_3', (3, 5, 7, 9)],['quantidade_col_3', (3, 5, 7, 10)],['quantidade_col_3', (3, 5, 7, 11)],['quantidade_col_3', (3, 5, 7, 12)],['quantidade_col_3', (3, 5, 7, 14)],['quantidade_col_3', (3, 5, 8, 9)],['quantidade_col_3', (3, 5, 8, 10)],['quantidade_col_3', (3, 5, 8, 11)],['quantidade_col_3', (3, 5, 8, 12)],['quantidade_col_3', (3, 5, 8, 13)],['quantidade_col_3', (3, 5, 8, 14)],['quantidade_col_3', (3, 5, 9, 12)],['quantidade_col_3', (3, 5, 9, 13)],['quantidade_col_3', (3, 5, 9, 14)],['quantidade_col_3', (3, 5, 10, 13)],['quantidade_col_3', (3, 5, 11, 12)],['quantidade_col_3', (3, 5, 11, 13)],['quantidade_col_3', (3, 5, 11, 14)],['quantidade_col_3', (3, 6, 7, 10)],['quantidade_col_3', (3, 6, 10, 13)],['quantidade_col_3', (3, 7, 8, 10)],['quantidade_col_3', (3, 7, 10, 11)],['quantidade_col_3', (3, 7, 10, 12)],['quantidade_col_3', (3, 7, 10, 13)],['quantidade_col_3', (3, 8, 10, 11)],['quantidade_col_3', (3, 8, 10, 13)],['quantidade_col_3', (4, 7, 9, 11)],['quantidade_col_3', (4, 9, 11, 13)],['quantidade_col_4', (0, 2, 8, 12)],['quantidade_col_4', (0, 4, 7, 12)],['quantidade_col_4', (0, 4, 8, 12)],['quantidade_col_4', (0, 5, 8, 10)],['quantidade_col_4', (0, 5, 8, 12)],['quantidade_col_4', (0, 6, 9, 13)],['quantidade_col_4', (1, 2, 8, 12)],['quantidade_col_4', (1, 4, 6, 9)],['quantidade_col_4', (1, 4, 7, 9)],['quantidade_col_4', (1, 4, 7, 12)],['quantidade_col_4', (1, 4, 8, 10)],['quantidade_col_4', (1, 5, 9, 12)],['quantidade_col_4', (1, 8, 10, 12)],['quantidade_col_4', (2, 4, 7, 10)],['quantidade_col_4', (2, 4, 7, 11)],['quantidade_col_4', (2, 4, 8, 10)],['quantidade_col_4', (2, 4, 8, 11)],['quantidade_col_4', (2, 4, 8, 12)],['quantidade_col_4', (2, 4, 10, 13)],['quantidade_col_4', (2, 5, 6, 11)],['quantidade_col_4', (2, 5, 10, 11)],['quantidade_col_4', (2, 5, 11, 14)],['quantidade_col_4', (2, 6, 8, 11)],['quantidade_col_4', (2, 8, 11, 12)],['quantidade_col_4', (2, 8, 12, 14)],['quantidade_col_4', (3, 5, 9, 12)],['quantidade_col_4', (3, 5, 10, 12)],['quantidade_col_4', (3, 5, 10, 13)],['quantidade_col_4', (4, 5, 10, 13)],['quantidade_col_4', (4, 7, 9, 12)],['quantidade_col_4', (4, 8, 9, 12)],['quantidade_col_4', (4, 8, 10, 13)],['quantidade_col_4', (5, 7, 11, 12)],['quantidade_col_4', (5, 10, 11, 13)],['quantidade_col_5', (1, 3, 5, 10)],['quantidade_col_5', (1, 3, 6, 9)],['quantidade_col_5', (1, 3, 8, 10)],['quantidade_col_5', (1, 4, 6, 11)],['quantidade_col_5', (1, 5, 10, 11)],['quantidade_col_5', (2, 4, 11, 13)],['quantidade_col_5', (2, 7, 11, 12)],['quantidade_col_5', (3, 4, 10, 12)],['quantidade_col_5', (3, 4, 10, 13)],['quantidade_col_5', (3, 6, 8, 12)],['quantidade_col_5', (3, 7, 8, 10)],['quantidade_col_5', (3, 7, 11, 14)]]
# for ca, po in lista:
# 	analise.compararCaracteristicaPosicao(ca, po)
		


for n in combinations(sorteios[-1].numeros, 2):
	print(n)
	print(analise.verificarNaoAcontecimentosPorNumeros(n, True))

# analise.print()