
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.Analise import *
from models.Sorteio import *
from models.Gerador import *
from libs.file_manager import lerSorteados

sorteios : list[Sorteio] = lerSorteados()
ultimo = sorteios[-1]
			
gerador = Gerador()

gerador.addRegra(ValidacaoAnalise.sequenciaRepetidaJogoAnterior, anterior = sorteios[-40])

gerador.addRegra(ValidacaoAnalise.compararSomaPosicoesPares, anterior = sorteios[-1])

gerador.addRegra(ValidacaoAnalise.compararSomaPosicoesImpares, anterior = sorteios[-1])

posicoes = [[1, 3, 6, 9] , [1, 3, 7, 12] , [2, 7, 11, 12] , [3, 5, 7, 12] , [3, 5, 9, 12] , [3, 5, 9, 13] , [3, 5, 10, 12] , [3, 5, 10, 13] , [3, 6, 7, 12] , [3, 6, 9, 12] , [3, 6, 10, 12] , [3, 6, 10, 13] , [3, 7, 8, 12] , [3, 7, 10, 12] , [3, 7, 10, 13] , [3, 7, 10, 14] , [3, 8, 10, 13], [3, 6, 12], [4,9], [4,10], [1, 3, 5, 6, 10], [1, 3, 5, 7, 10], [1, 3, 5, 9, 14], [1, 3, 5, 10, 14], [1, 3, 7, 8, 14], [1, 3, 7, 9, 14], [1, 5, 6, 10, 11], [1, 5, 7, 10, 11], [1, 5, 9, 10, 11], [1, 5, 9, 11, 14], [1, 5, 10, 11, 14], [2, 3, 5, 7, 10], [2, 3, 7, 8, 14], [2, 4, 7, 8, 11], [2, 5, 7, 10, 11], [2, 5, 9, 11, 12], [2, 6, 8, 11, 12], [2, 6, 9, 11, 12], [2, 7, 9, 11, 14], [2, 8, 9, 11, 12], [3, 6, 9, 13, 14], [3, 7, 11, 12, 14], [3, 8, 9, 11, 12], [3, 8, 9, 13, 14], [6, 7, 10, 11, 13], [6, 8, 10, 11, 12], [6, 8, 10, 11, 13]]
for p in posicoes:
	gerador.addRegra(ValidacaoAnalise.compararChavePosicoes, anterior = sorteios[-1], posicoes = p )

posicoes = [[0, 4, 6, 7, 8],[1, 2, 5, 8, 13], [0, 8, 10, 13], [0, 6, 8, 10]]
for p in posicoes:
	gerador.addRegra(ValidacaoAnalise.compararChavePosicoesComAnterior, anterior = sorteios[-1], posicoes = p )

gerador.addRegra(ValidacaoAnalise.compararSomas, anterior = sorteios[-1])

gerador.addRegra(ValidacaoAnalise.compararMultiplicacoes, anterior = sorteios[-1])

caracteristicas = [('soma_pares', 'soma_impares'), ('soma_pares', 'soma_primos'), ('soma_pares', 'soma_menores_13'), ('soma_impares', 'soma_menores_10'), ('soma_impares', 'soma_entre_10_20'), ('soma_impares', 'soma_maiores_20'), ('soma_impares', 'soma_menores_13'), ('soma_impares', 'soma_maiores_13'), ('soma_impares', 'soma_meio'), ('soma_impares', 'soma_col_2'), ('soma_impares', 'soma_col_3'), ('soma_menores_10', 'soma_primos'), ('soma_menores_10', 'soma_maiores_13'), ('soma_entre_10_20', 'soma_menores_13'), ('soma_entre_10_20', 'soma_col_1'), ('soma_entre_10_20', 'soma_col_2'), ('soma_maiores_20', 'soma_primos'), ('soma_primos', 'soma_menores_13'), ('soma_primos', 'soma_maiores_13'), ('soma_primos', 'soma_meio'), ('soma_menores_13', 'soma_maiores_13'), ('soma_menores_13', 'soma_meio'), ('soma_maiores_13', 'soma_col_1'), ('soma_maiores_13', 'soma_col_3'), ('soma_maiores_13', 'soma_col_4'), ('soma_meio', 'soma_col_3'), ('soma_impares',), ('soma_maiores_13',)]
for c in caracteristicas:
	gerador.addRegra(ValidacaoAnalise.compararCaracteristicas, anterior = sorteios[-1], caracteristicas = c)


gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 0, minimo = 1, maximo = 5)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 1, minimo = 2, maximo = 7)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 2, minimo = 3, maximo = 9)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 3, minimo = 4, maximo = 11)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 4, minimo = 5, maximo = 12)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 5, minimo = 6, maximo = 14)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 6, minimo = 7, maximo = 16)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 7, minimo = 9, maximo = 17)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 8, minimo = 10, maximo = 19)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 9, minimo = 11, maximo = 20)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 10, minimo = 13, maximo = 21)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 11, minimo = 15, maximo = 22)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 12, minimo = 17, maximo = 23)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 13, minimo = 18, maximo = 24)
gerador.addRegra(ValidacaoAnalise.verificarPossibilidadePosicao, posicao = 14, minimo = 20, maximo = 25)

gerador.addRegra(ValidacaoAnalise.quantidadeRepetida, anterior = sorteios[-1])

gerador.addRegra(ValidacaoAnalise.verificarMaximaDiferencaVizinhos, minimo = 2, maximo = 7)

gerador.addRegra(ValidacaoAnalise.verificarTamanhoMaximoSequencia, minimo = 2, maximo = 10)


gerador.addRegra(ValidacaoAnalise.verificarCaracteristica, caracteristica = 'pares', minimo = 4, maximo = 10)
gerador.addRegra(ValidacaoAnalise.verificarCaracteristica, caracteristica = 'quantidade_primos', minimo = 2, maximo = 8)
gerador.addRegra(ValidacaoAnalise.verificarCaracteristica, caracteristica = 'quantidade_menores_10', minimo = 2, maximo = 8)
gerador.addRegra(ValidacaoAnalise.verificarCaracteristica, caracteristica = 'quantidade_entre_10_20', minimo = 3, maximo = 9)
gerador.addRegra(ValidacaoAnalise.verificarCaracteristica, caracteristica = 'quantidade_maiores_20', minimo = 1, maximo = 5)
gerador.addRegra(ValidacaoAnalise.verificarCaracteristica, caracteristica = 'quantidade_meio', minimo = 2, maximo = 8)
gerador.addRegra(ValidacaoAnalise.verificarCaracteristica, caracteristica = 'quantidade_menores_13', minimo = 4, maximo = 10)

gerador.addRegra(ValidacaoAnalise.verificarCaracteristica, caracteristica = 'quantidade_col_1', minimo = 1, maximo = 5)
gerador.addRegra(ValidacaoAnalise.verificarCaracteristica, caracteristica = 'quantidade_col_2', minimo = 1, maximo = 5)
gerador.addRegra(ValidacaoAnalise.verificarCaracteristica, caracteristica = 'quantidade_col_3', minimo = 1, maximo = 5)
gerador.addRegra(ValidacaoAnalise.verificarCaracteristica, caracteristica = 'quantidade_col_4', minimo = 1, maximo = 5)
gerador.addRegra(ValidacaoAnalise.verificarCaracteristica, caracteristica = 'quantidade_col_5', minimo = 1, maximo = 5)

sorteios_anteriores = [x.numeros for x in sorteios]
gerador.addRegra(ValidacaoAnalise.verificarContem, lista = sorteios_anteriores)


# gerador.buscarNumeros(86)

gerador.analisarSorteio([4,5,6,7,8,9,14,18,19,20,21,22,23,24,25])

## RESUMO
# Jogos Realizados: 86
# Jogos com acerto:
# Eficácia: 