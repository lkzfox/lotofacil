from models.Analise import *
from models.Sorteio import *
from models.Gerador import *
from libs.helper import obterTodasSequencias, intersecao, buscarQuantidadesSequencias, chaveNumeros, resolver, fatorarAnteriores, resolverSimples, buscarNumerosCaminho, caminhoValido, chaveSequenciaPulo, todasSequenciasPulos, quantidadeNumerosIrmaos, todasSequenciasPares, todasSquenciasTamanho, analisarLista, contemSquenciaCrescente
from libs.file_manager import lerSorteados
from libs.data_process import gerarDicionarioSimples, gerarSorteioSimples
import pprint
from itertools import combinations, permutations
import pandas as pd
import random
import re
import io

sorteios = lerSorteados()[:]
total = len(sorteios)
ultimo = sorteios[-1]
analise = Analise(sorteios[:])
gerador = Gerador()
contador, menor, maior = 0, 999999, 0
# analise.compararFatoracaoSorteiosAnteriores(3, 13)


# def buscarCombos(quantidade, numeros, jogos, numeros_saindo = True, visao_geral = False):
#     combinacoes = list(combinations(numeros, quantidade))
#     final = {}
#     for comb in combinacoes:
#         chave = '.'.join([str(x) for x in comb])
#         final[chave] = {'ocorrencias': 0, 'numeros': list(range(26)), 'nunca': list(range(26))}
#     for n in range(len(jogos)-1):
#         numeros_jogo = jogos[n].numeros
#         numeros_proximo_jogo = jogos[n+1].numeros
#         for comb in combinacoes:
#             chave = '.'.join([str(x) for x in comb])
#             if len(intersecao(comb, numeros_jogo)) == len(comb):
#                 final[chave]['numeros'] = intersecao(final[chave]['numeros'], numeros_proximo_jogo)
#                 final[chave]['nunca']   = intersecao(final[chave]['nunca'], [x for x in range(1,26) if x not in numeros_proximo_jogo])
#                 final[chave]['ocorrencias'] = final[chave]['ocorrencias'] + 1
    
#     if not visao_geral:
#         final = dict(sorted(final.items(), key=lambda x: x[1]['ocorrencias'], reverse=True))
#         for chave, valor in final.items():
#             if len(valor['numeros']) == 1 and numeros_saindo: print(chave, valor)
#             if len(valor['nunca']) == 1 and (not numeros_saindo): print(chave, valor)
#     else:
#         final = dict(sorted(final.items(), key=lambda x: x[1]['ocorrencias'], reverse=False))
#         for chave, valor in final.items():
#             print(chave, valor)


# # Buscar as combinações de números que mais sairam para as dezenas do último jogo
# buscarCombos(2, ultimo.numeros, sorteios[-20:])
# print('=====================================')
# buscarCombos(3, ultimo.numeros, sorteios[-20:])
# print('-----------------------------------')
# # Buscar as combinações de números que nunca sairam para as dezenas do último jogo, tem que te pelo menos 5 ocorrências
# buscarCombos(2, ultimo.numeros, sorteios[-15:], False)
# print('=====================================')
# buscarCombos(3, ultimo.numeros, sorteios[-15:], False)

# exit()


def todasCombs(tamanho = 2, valor_maximo = 15, intervalo_minimo = 3):
	combs = list(combinations(range(0, valor_maximo+1), 2))
	combs = [passo for passo in combs if passo[1] - passo[0] >= intervalo_minimo and passo[1] - passo[0] < 7]
	possiveis = list(combinations(combs, tamanho))

	return possiveis

# analise.verificarRankqueamentoColunas()
# exit()

p = ['-','+','-','+','-','+','-','+','-','+','-','+','-','+','-','+','-','+','-','+','-','+',]
combs = list(permutations(p,1))
# combs = [sorted(x) for x in combs]
combs = list(set(['.'.join([str(y) for y in x]) for x in combs]))
combs = [[y for y in str(x).split('.')] for x in combs]
total_combs = len(combs)
# for somas in combs:
# 	for posicoes2 in combinations(range(15),2):
# for operacoes in combs:
# 	contador += 1
combs= list(combinations(range(15),5))
total_combs = len(combs)
for posicoes in combs:
	contador += 1
	for tamanho in range(5,11):
		ret = analise.verificarRankqueamentoColunas(tamanho, posicoes, True)
		qtd = ret['Qtd Igual']
		if qtd > 0:
			menor = min(menor, qtd)
			maior = max(maior, qtd)
		print(str(tamanho).ljust(12, ' '), str(qtd).ljust(5,' '), str(f'{contador}/{total_combs}').ljust(20), menor, maior, end='                                   \r')
		# considerar tambem o qtd == 11, pra ver a media
		if qtd > 0 and (qtd < 2 or qtd > 3173):# and ret['media'] > 11:
			print(end='\r'.rjust(80,' '))
			pprint.pp(ret)
exit()

# lista = [[(1, 10, 11, 12), [1, 2, 3, 4]],[(2, 10, 11, 12), [1, 2, 3, 4]],[(3, 10, 11, 12), [1, 2, 3, 4]],[(4, 10, 11, 12), [1, 2, 3, 4]],[(5, 10, 11, 12), [1, 2, 3, 4]],[(6, 10, 11, 12), [1, 2, 3, 4]],[(7, 10, 11, 12), [1, 2, 3, 4]],[(8, 10, 11, 12), [1, 2, 3, 4]],[(9, 10, 11, 12), [1, 2, 3, 4]]]
# for [ posicoes, somas ] in lista:
# 	gerador.addRegra(ValidacaoAnalise.verificarPosicaoSomaValores, posicoes = posicoes, somas = somas)

# lista = [[7, (1, 4, 11), ['+', '+']],[7, (1, 6, 7), ['+', '+']],[7, (2, 3, 6), ['+', '+']],[7, (2, 4, 6), ['+', '+']],[7, (2, 6, 7), ['+', '+']],[7, (2, 7, 8), ['+', '+']],[7, (2, 8, 12), ['+', '+']],[7, (3, 4, 7), ['+', '+']],[7, (3, 4, 9), ['+', '+']],[7, (3, 5, 6), ['+', '+']],[7, (3, 6, 11), ['+', '+']],[7, (4, 6, 8), ['+', '+']],[7, (4, 6, 10), ['+', '+']],[7, (4, 9, 10), ['+', '+']],[7, (5, 6, 8), ['+', '+']],[7, (5, 6, 9), ['+', '+']],[7, (5, 7, 8), ['+', '+']],[7, (5, 8, 13), ['+', '+']],[7, (6, 9, 11), ['+', '+']],[7, (6, 9, 14), ['+', '+']],[7, (8, 9, 12), ['+', '+']],[7, (8, 9, 14), ['+', '+']],[6, (6, 9, 11), ['+', '+']]]
# for [tamanho, posicoes, operacoes ] in lista:
# 	gerador.addRegra(ValidacaoAnalise.compararOperacoesPosicoesV2, anteriores = sorteios[-tamanho:], posicoes = posicoes, operacoes = operacoes)

# lista = [[5, (1, 3, 8)],[6, (1, 4, 10)],[3, (1, 4, 11)],[6, (1, 6, 10)],[7, (1, 6, 10)],[6, (1, 7, 10)],[4, (1, 7, 11)],[5, (1, 7, 11)],[4, (2, 4, 12)],[3, (2, 5, 9)],[6, (2, 5, 9)],[2, (2, 5, 10)],[5, (2, 5, 10)],[3, (2, 5, 12)],[7, (2, 6, 9)],[5, (2, 6, 12)],[7, (2, 6, 12)],[6, (2, 8, 12)],[3, (3, 4, 11)],[7, (3, 6, 8)],[7, (3, 6, 9)],[3, (3, 6, 11)],[6, (3, 6, 11)],[3, (3, 6, 12)],[6, (3, 7, 9)],[4, (3, 8, 12)],[7, (3, 8, 12)],[6, (3, 11, 13)],[6, (4, 5, 11)],[3, (4, 6, 11)],[6, (4, 6, 11)],[3, (4, 8, 11)],[4, (4, 8, 11)],[5, (4, 8, 11)],[6, (4, 8, 11)],[2, (4, 9, 12)],[4, (4, 9, 12)],[7, (4, 10, 13)],[6, (5, 8, 10)],[2, (5, 8, 12)],[3, (5, 8, 12)],[5, (6, 9, 11)]]
# for [tamanho, posicoes ] in lista:
# 	gerador.addRegra(ValidacaoAnalise.verificarChaveDiferencaAnterior, anteriores = sorteios[-tamanho:], posicoes = posicoes)



# gerador.calcularReducao(10000)
# gerador.buscarNumerosTeste()

if True:
	gerador.analisarSorteio([3,4,5,6,10,12,13,15,16,18,19,21,22,23,25])
	print('-------------------------------------------------')
	gerador.analisarSorteio([3, 4, 5, 7, 8, 9, 10, 12, 13, 15, 16, 19, 21, 24, 25])
	gerador.analisarSorteio([1, 2, 5, 7, 8, 10, 11, 12, 13, 15, 18, 21, 22, 24, 25])
	gerador.analisarSorteio([1, 3, 4, 6, 7, 8, 11, 12, 14, 15, 17, 18, 21, 22, 25])
	gerador.analisarSorteio([1, 3, 4, 7, 8, 10, 11, 12, 14, 15, 17, 21, 22, 23, 24])
	gerador.analisarSorteio([1, 3, 5, 6, 7, 9, 10, 11, 12, 13, 17, 20, 22, 24, 25])
	gerador.analisarSorteio([1, 3, 5, 7, 8, 9, 10, 12, 13, 16, 17, 19, 21, 22, 23])
	gerador.analisarSorteio([1, 2, 5, 7, 8, 9, 11, 12, 13, 14, 17, 21, 23, 24, 25])
	gerador.analisarSorteio([1, 4, 5, 6, 7, 9, 10, 11, 12, 14, 16, 19, 23, 24, 25])
	gerador.analisarSorteio([1, 2, 6, 7, 8, 9, 10, 11, 13, 14, 17, 19, 20, 21, 24])
	gerador.analisarSorteio([1, 4, 5, 6, 7, 8, 11, 12, 13, 15, 19, 20, 21, 22, 23])
	gerador.analisarSorteio([1, 3, 4, 5, 8, 9, 11, 12, 14, 15, 16, 19, 21, 24, 25])
	gerador.analisarSorteio([1, 3, 5, 7, 8, 9, 11, 12, 13, 14, 18, 20, 21, 23, 25])
	gerador.analisarSorteio([1, 2, 4, 5, 6, 8, 9, 12, 14, 17, 18, 19, 20, 24, 25])
	gerador.analisarSorteio([1, 3, 5, 6, 7, 9, 10, 11, 12, 13, 15, 20, 22, 23, 24])
	gerador.analisarSorteio([3, 4, 5, 6, 7, 9, 10, 11, 15, 17, 18, 20, 21, 23, 24])
	gerador.analisarSorteio([1, 3, 4, 5, 7, 8, 9, 10, 13, 17, 18, 21, 23, 24, 25])
	gerador.analisarSorteio([1, 4, 6, 7, 8, 9, 10, 11, 13, 14, 17, 19, 21, 23, 25])
	gerador.analisarSorteio([1, 2, 5, 6, 8, 9, 11, 12, 13, 14, 15, 20, 21, 22, 25])
	gerador.analisarSorteio([1, 2, 3, 5, 7, 9, 10, 11, 12, 14, 15, 16, 21, 24, 25])
	gerador.analisarSorteio([1, 4, 5, 6, 8, 9, 10, 11, 13, 14, 17, 20, 21, 23, 25])
	gerador.analisarSorteio([1, 2, 3, 5, 7, 9, 10, 11, 12, 16, 18, 19, 21, 24, 25])
	gerador.analisarSorteio([1, 3, 4, 8, 9, 10, 11, 12, 14, 15, 16, 19, 20, 23, 24])
	gerador.analisarSorteio([1, 2, 5, 6, 7, 9, 11, 12, 13, 14, 16, 18, 20, 23, 25])
	gerador.analisarSorteio([1, 4, 5, 7, 9, 10, 11, 12, 13, 16, 17, 18, 21, 22, 23])
	gerador.analisarSorteio([3, 5, 6, 8, 9, 10, 11, 12, 15, 16, 17, 21, 22, 24, 25])
	gerador.analisarSorteio([3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15, 18, 21, 24, 25])

print('')
exit()





tamanho_sorteios = len(sorteios)
for idx in range(tamanho_sorteios - 12, len(sorteios)):
	_sorteios = sorteios[:idx]
	analise = Analise(_sorteios)
	ultimo = sorteios[idx]

	lista = [[1, (1, 12), [-1, -4]],[1, (1, 13), [-1, -4]],[1, (3, 13), [-1, -4]],[1, (5, 13), [-1, -4]],[1, (6, 13), [-1, -4]],[1, (8, 13), [-1, -4]],[1, (1, 2), [-5, -3]],[1, (1, 3), [-5, -3]],[1, (1, 5), [-5, -3]],[1, (1, 6), [-5, -3]],[1, (1, 7), [-5, -3]],[1, (1, 8), [-5, -3]],[1, (2, 5), [-5, -3]],[1, (2, 8), [-5, -3]],[1, (2, 11), [-5, -3]],[1, (2, 13), [-5, -3]],[1, (3, 9), [-5, -3]],[1, (3, 10), [-5, -3]],[1, (3, 13), [-5, -3]],[1, (4, 10), [-5, -3]],[1, (4, 13), [-5, -3]],[1, (5, 11), [-5, -3]],[1, (6, 11), [-5, -3]],[1, (7, 8), [-5, -3]],[1, (10, 11), [-5, -3]],[1, (10, 12), [-5, -3]],[1, (12, 13), [-5, -3]],[1, (2, 12), [-4, 5]],[1, (2, 13), [-4, 5]],[1, (4, 7), [-4, 5]],[1, (4, 9), [-4, 5]],[1, (7, 13), [4, -2]],[1, (2, 11), [4, -4]],[1, (3, 11), [4, -4]],[1, (4, 5), [4, -4]],[1, (9, 10), [4, -4]],[1, (11, 12), [1, 5]],[1, (2, 4), [-3, 3]],[1, (3, 4), [-3, 3]],[1, (3, 5), [-3, 3]],[1, (4, 6), [-3, 3]],[1, (4, 8), [-3, 3]],[1, (7, 9), [-3, 3]],[1, (8, 9), [-3, 3]],[1, (8, 10), [-3, 3]],[1, (9, 11), [-3, 3]],[1, (1, 10), [4, -3]],[1, (1, 12), [4, -3]],[1, (1, 13), [4, -3]],[1, (1, 9), [5, -3]],[1, (2, 11), [5, -3]],[1, (2, 12), [5, -3]],[1, (3, 10), [5, -3]],[1, (3, 12), [5, -3]],[1, (1, 13), [-2, -2]],[1, (1, 2), [-3, 1]],[1, (1, 3), [-3, 1]],[1, (4, 5), [-3, 1]],[1, (6, 7), [-3, 1]],[1, (9, 10), [-3, 1]],[1, (3, 11), [-2, -4]],[1, (3, 12), [-2, -4]],[1, (3, 13), [-2, -4]],[1, (4, 13), [-2, -4]],[1, (6, 13), [-2, -4]],[1, (8, 13), [-2, -4]],[1, (10, 13), [-2, -4]],[1, (1, 13), [0, -4]],[1, (2, 13), [0, -4]],[1, (2, 11), [1, -5]],[1, (3, 11), [1, -5]],[1, (1, 10), [-2, -5]],[1, (3, 10), [-2, -5]],[1, (3, 11), [-2, -5]],[1, (4, 11), [-2, -5]],[1, (5, 10), [-2, -5]],[1, (5, 11), [-2, -5]],[1, (8, 12), [-2, -5]],[1, (1, 3), [-4, 1]],[1, (1, 5), [-4, 1]],[1, (2, 7), [-4, 1]],[1, (2, 8), [-4, 1]],[1, (2, 11), [-4, 1]],[1, (5, 7), [-4, 1]],[1, (6, 7), [-4, 1]],[1, (6, 8), [-4, 1]],[1, (8, 9), [-4, 1]],[1, (9, 10), [-4, 1]],[1, (10, 11), [-4, 1]],[1, (1, 11), [-1, -5]],[1, (1, 12), [-1, -5]],[1, (3, 12), [-1, -5]],[1, (4, 12), [-1, -5]],[1, (5, 12), [-1, -5]],[1, (1, 10), [5, -2]],[1, (1, 12), [5, -2]],[1, (1, 13), [5, -2]],[1, (3, 12), [5, -2]],[1, (3, 13), [5, -2]],[1, (1, 2), [5, -4]],[1, (2, 10), [5, -4]],[1, (3, 4), [5, -4]],[1, (6, 7), [5, -4]],[1, (7, 8), [5, -4]],[1, (11, 12), [5, -4]],[1, (12, 13), [5, -4]],[1, (3, 4), [-2, 3]],[1, (3, 5), [-2, 3]],[1, (4, 6), [-2, 3]],[1, (8, 9), [-2, 3]],[1, (9, 10), [-2, 3]],[1, (11, 12), [-2, 3]],[1, (1, 4), [-2, 5]],[1, (1, 8), [-2, 5]],[1, (2, 4), [-2, 5]],[1, (2, 7), [-2, 5]],[1, (2, 9), [-2, 5]],[1, (2, 12), [-2, 5]],[1, (3, 6), [-2, 5]],[1, (3, 7), [-2, 5]],[1, (3, 10), [-2, 5]],[1, (3, 11), [-2, 5]],[1, (3, 13), [-2, 5]],[1, (4, 6), [-2, 5]],[1, (4, 13), [-2, 5]],[1, (5, 9), [-2, 5]],[1, (6, 9), [-2, 5]],[1, (6, 10), [-2, 5]],[1, (7, 9), [-2, 5]],[1, (7, 10), [-2, 5]],[1, (7, 13), [-2, 5]],[1, (9, 12), [-2, 5]],[1, (10, 13), [-2, 5]],[1, (1, 12), [-4, -4]],[1, (2, 9), [-4, -4]],[1, (7, 13), [-4, -4]],[1, (1, 4), [-4, 2]],[1, (1, 5), [-4, 2]],[1, (1, 6), [-4, 2]],[1, (2, 5), [-4, 2]],[1, (2, 7), [-4, 2]],[1, (4, 7), [-4, 2]],[1, (5, 7), [-4, 2]],[1, (5, 9), [-4, 2]],[1, (6, 7), [-4, 2]],[1, (6, 9), [-4, 2]],[1, (10, 11), [-4, 2]],[1, (12, 13), [-4, 2]],[1, (6, 13), [2, -5]],[1, (10, 11), [-2, 2]],[1, (4, 13), [3, -3]],[1, (1, 2), [-3, 0]],[1, (1, 13), [2, -4]],[1, (2, 13), [2, -4]],[1, (3, 13), [2, -4]],[1, (4, 12), [2, -4]],[1, (5, 12), [2, -4]],[1, (1, 10), [-3, -1]],[1, (1, 12), [-3, -1]],[1, (1, 13), [-3, -1]],[1, (1, 9), [3, -5]],[1, (3, 4), [3, -5]],[1, (11, 12), [3, -5]],[1, (2, 11), [5, -5]],[1, (3, 12), [5, -5]],[1, (1, 10), [-3, -2]],[1, (1, 12), [-3, -2]],[1, (1, 13), [-3, -2]],[1, (1, 13), [5, -1]],[1, (2, 3), [-4, -2]],[1, (7, 13), [-4, -2]],[1, (12, 13), [-1, 3]],[1, (2, 7), [-3, -4]],[1, (2, 9), [-3, -4]],[1, (3, 12), [-3, -4]],[1, (4, 10), [-3, -4]],[1, (4, 11), [-3, -4]],[1, (4, 12), [-3, -4]],[1, (5, 12), [-3, -4]],[1, (8, 13), [-3, -4]],[1, (11, 13), [-3, -4]],[1, (1, 6), [-5, -1]],[1, (1, 12), [-5, -1]],[1, (2, 6), [-5, -1]],[1, (2, 9), [-5, -1]],[1, (2, 10), [-5, -1]],[1, (2, 13), [-5, -1]],[1, (3, 7), [-5, -1]],[1, (3, 9), [-5, -1]],[1, (3, 12), [-5, -1]],[1, (3, 13), [-5, -1]],[1, (4, 11), [-5, -1]],[1, (5, 12), [-5, -1]],[1, (7, 8), [-5, -1]],[1, (8, 9), [-5, -1]],[1, (9, 13), [-5, -1]],[1, (12, 13), [-5, -1]],[1, (1, 5), [-3, -5]],[1, (1, 6), [-3, -5]],[1, (1, 7), [-3, -5]],[1, (1, 8), [-3, -5]],[1, (1, 11), [-3, -5]],[1, (2, 9), [-3, -5]],[1, (2, 11), [-3, -5]],[1, (6, 10), [-3, -5]],[1, (7, 11), [-3, -5]],[1, (8, 11), [-3, -5]],[1, (8, 12), [-3, -5]],[1, (1, 8), [-4, 3]],[1, (1, 11), [-4, 3]],[1, (1, 13), [-4, 3]],[1, (2, 8), [-4, 3]],[1, (2, 11), [-4, 3]],[1, (2, 13), [-4, 3]],[1, (3, 8), [-4, 3]],[1, (4, 9), [-4, 3]],[1, (5, 9), [-4, 3]],[1, (6, 9), [-4, 3]],[1, (7, 9), [-4, 3]],[1, (7, 10), [-4, 3]],[1, (8, 10), [-4, 3]],[1, (9, 11), [-4, 3]],[1, (9, 12), [-4, 3]],[1, (6, 9), [-1, 5]],[1, (8, 9), [-1, 5]],[1, (8, 10), [-1, 5]],[1, (9, 12), [-1, 5]],[1, (11, 13), [-1, 5]],[1, (1, 5), [-3, 2]],[1, (2, 5), [-3, 2]],[1, (4, 5), [-3, 2]],[1, (6, 7), [-3, 2]],[1, (10, 11), [-3, 2]],[1, (12, 13), [-3, 2]],[1, (1, 2), [-1, 4]],[1, (2, 3), [-1, 4]],[1, (3, 4), [-1, 4]],[1, (4, 5), [-1, 4]],[1, (6, 7), [-1, 4]],[1, (9, 11), [-1, 4]],[1, (10, 11), [-1, 4]],[1, (1, 4), [-4, -1]],[1, (1, 6), [-4, -1]],[1, (1, 9), [-4, -1]],[1, (2, 3), [-4, -1]],[1, (5, 6), [-4, -1]],[1, (11, 12), [-4, -1]],[1, (12, 13), [-4, -1]],[1, (1, 13), [3, -4]],[1, (2, 10), [3, -4]],[1, (2, 11), [3, -4]],[1, (2, 13), [3, -4]],[1, (5, 12), [3, -4]],[1, (6, 13), [3, -4]],[1, (5, 11), [-5, 3]],[1, (5, 12), [-5, 3]],[1, (6, 11), [-5, 3]],[1, (6, 12), [-5, 3]],[1, (8, 12), [-5, 3]],[1, (8, 13), [-5, 3]],[1, (1, 9), [-4, -3]],[1, (1, 10), [-4, -3]],[1, (1, 13), [-4, -3]],[1, (3, 11), [-4, -3]],[1, (3, 13), [-4, -3]],[1, (4, 11), [-4, -3]],[1, (4, 13), [-4, -3]],[1, (5, 13), [-4, -3]],[1, (6, 13), [-4, -3]],[1, (7, 13), [-4, -3]],[1, (5, 11), [-5, 4]],[1, (6, 11), [-5, 4]],[1, (1, 11), [0, -5]],[1, (2, 11), [0, -5]],[1, (3, 11), [0, -5]],[1, (4, 11), [0, -5]],[1, (5, 11), [0, -5]],[1, (12, 13), [0, -5]],[1, (3, 4), [0, 5]],[1, (4, 5), [0, 5]],[1, (7, 8), [0, 5]],[1, (8, 9), [0, 5]],[1, (8, 11), [0, 5]],[1, (9, 10), [0, 5]],[1, (12, 13), [0, 5]],[1, (1, 7), [-5, -5]],[1, (1, 8), [-5, -5]],[1, (2, 4), [-5, -5]],[1, (2, 5), [-5, -5]],[1, (2, 6), [-5, -5]],[1, (2, 7), [-5, -5]],[1, (2, 9), [-5, -5]],[1, (2, 10), [-5, -5]],[1, (4, 8), [-5, -5]],[1, (4, 9), [-5, -5]],[1, (4, 11), [-5, -5]],[1, (5, 12), [-5, -5]],[1, (6, 9), [-5, -5]],[1, (6, 12), [-5, -5]],[1, (7, 10), [-5, -5]],[1, (1, 2), [-5, 0]],[1, (1, 5), [-5, 0]],[1, (1, 7), [-5, 0]],[1, (1, 8), [-5, 0]],[1, (1, 12), [-5, 0]],[1, (2, 4), [-5, 0]],[1, (2, 7), [-5, 0]],[1, (2, 8), [-5, 0]],[1, (2, 11), [-5, 0]],[1, (2, 12), [-5, 0]],[1, (3, 5), [-5, 0]],[1, (4, 7), [-5, 0]],[1, (4, 13), [-5, 0]],[1, (5, 13), [-5, 0]],[1, (8, 9), [-5, 0]],[1, (9, 11), [-5, 0]],[1, (10, 11), [-5, 0]],[1, (11, 13), [-5, 0]],[1, (12, 13), [-5, 0]],[1, (2, 13), [1, -4]],[1, (5, 13), [1, -4]],[1, (6, 13), [1, -4]],[1, (1, 8), [-3, -3]],[1, (1, 9), [-3, -3]],[1, (1, 12), [-3, -3]],[1, (2, 12), [-3, -3]],[1, (3, 11), [-3, -3]],[1, (3, 12), [-3, -3]],[1, (3, 13), [-3, -3]],[1, (1, 6), [-5, -4]],[1, (1, 9), [-5, -4]],[1, (1, 10), [-5, -4]],[1, (2, 7), [-5, -4]],[1, (2, 9), [-5, -4]],[1, (2, 10), [-5, -4]],[1, (2, 11), [-5, -4]],[1, (3, 7), [-5, -4]],[1, (3, 8), [-5, -4]],[1, (3, 12), [-5, -4]],[1, (4, 6), [-5, -4]],[1, (4, 7), [-5, -4]],[1, (4, 9), [-5, -4]],[1, (4, 11), [-5, -4]],[1, (4, 12), [-5, -4]],[1, (5, 9), [-5, -4]],[1, (5, 12), [-5, -4]],[1, (6, 12), [-5, -4]],[1, (7, 11), [-5, -4]],[1, (7, 12), [-5, -4]],[1, (8, 13), [-5, -4]],[1, (9, 13), [-5, -4]],[1, (10, 13), [-5, -4]],[1, (11, 12), [-5, -4]],[1, (3, 13), [3, -2]],[1, (1, 3), [-5, 1]],[1, (1, 4), [-5, 1]],[1, (1, 6), [-5, 1]],[1, (1, 7), [-5, 1]],[1, (1, 9), [-5, 1]],[1, (1, 11), [-5, 1]],[1, (1, 13), [-5, 1]],[1, (2, 8), [-5, 1]],[1, (2, 9), [-5, 1]],[1, (3, 6), [-5, 1]],[1, (3, 7), [-5, 1]],[1, (3, 10), [-5, 1]],[1, (4, 8), [-5, 1]],[1, (4, 9), [-5, 1]],[1, (6, 7), [-5, 1]],[1, (6, 9), [-5, 1]],[1, (9, 10), [-5, 1]],[1, (9, 11), [-5, 1]],[1, (10, 12), [-5, 1]],[1, (1, 7), [-4, 4]],[1, (1, 11), [-4, 4]],[1, (1, 12), [-4, 4]],[1, (1, 13), [-4, 4]],[1, (2, 6), [-4, 4]],[1, (2, 8), [-4, 4]],[1, (2, 9), [-4, 4]],[1, (2, 10), [-4, 4]],[1, (2, 12), [-4, 4]],[1, (3, 7), [-4, 4]],[1, (3, 11), [-4, 4]],[1, (3, 12), [-4, 4]],[1, (4, 10), [-4, 4]],[1, (5, 9), [-4, 4]],[1, (5, 11), [-4, 4]],[1, (5, 12), [-4, 4]],[1, (5, 13), [-4, 4]],[1, (6, 9), [-4, 4]],[1, (6, 11), [-4, 4]],[1, (6, 12), [-4, 4]],[1, (7, 9), [-4, 4]],[1, (7, 11), [-4, 4]],[1, (1, 9), [-3, 4]],[1, (1, 10), [-3, 4]],[1, (2, 6), [-3, 4]],[1, (2, 8), [-3, 4]],[1, (3, 6), [-3, 4]],[1, (3, 7), [-3, 4]],[1, (3, 8), [-3, 4]],[1, (3, 11), [-3, 4]],[1, (5, 10), [-3, 4]],[1, (6, 9), [-3, 4]],[1, (6, 13), [-3, 4]],[1, (8, 9), [-3, 4]],[1, (9, 11), [-3, 4]],[1, (9, 12), [-3, 4]],[1, (9, 13), [-3, 4]],[1, (10, 13), [-3, 4]],[1, (1, 2), [4, -5]],[1, (1, 10), [4, -5]],[1, (2, 3), [4, -5]],[1, (2, 10), [4, -5]],[1, (2, 11), [4, -5]],[1, (4, 12), [4, -5]],[1, (6, 7), [4, -5]],[1, (9, 10), [4, -5]],[1, (11, 12), [4, -5]],[1, (12, 13), [4, -5]],[1, (1, 4), [-5, -2]],[1, (1, 9), [-5, -2]],[1, (1, 10), [-5, -2]],[1, (2, 4), [-5, -2]],[1, (2, 7), [-5, -2]],[1, (3, 4), [-5, -2]],[1, (3, 12), [-5, -2]],[1, (4, 5), [-5, -2]],[1, (4, 12), [-5, -2]],[1, (5, 6), [-5, -2]],[1, (5, 13), [-5, -2]],[1, (6, 7), [-5, -2]],[1, (7, 8), [-5, -2]],[1, (7, 13), [-5, -2]],[1, (8, 13), [-5, -2]],[1, (10, 11), [-5, -2]],[1, (10, 13), [-5, -2]],[1, (11, 12), [-5, -2]],[1, (12, 13), [-5, -2]],[1, (1, 4), [-4, -5]],[1, (1, 5), [-4, -5]],[1, (2, 8), [-4, -5]],[1, (2, 10), [-4, -5]],[1, (2, 11), [-4, -5]],[1, (2, 12), [-4, -5]],[1, (3, 8), [-4, -5]],[1, (3, 9), [-4, -5]],[1, (3, 10), [-4, -5]],[1, (4, 9), [-4, -5]],[1, (5, 10), [-4, -5]],[1, (6, 11), [-4, -5]],[1, (10, 12), [-4, -5]],[1, (1, 7), [-4, 0]],[1, (1, 10), [-4, 0]],[1, (2, 5), [-4, 0]],[1, (3, 4), [-4, 0]],[1, (1, 8), [-5, 2]],[1, (1, 9), [-5, 2]],[1, (1, 11), [-5, 2]],[1, (1, 13), [-5, 2]],[1, (2, 8), [-5, 2]],[1, (2, 11), [-5, 2]],[1, (3, 8), [-5, 2]],[1, (3, 9), [-5, 2]],[1, (4, 7), [-5, 2]],[1, (4, 8), [-5, 2]],[1, (5, 9), [-5, 2]],[1, (6, 10), [-5, 2]],[1, (7, 10), [-5, 2]],[1, (7, 12), [-5, 2]],[1, (8, 11), [-5, 2]],[1, (2, 8), [-3, 5]],[1, (2, 9), [-3, 5]],[1, (3, 7), [-3, 5]],[1, (3, 9), [-3, 5]],[1, (3, 11), [-3, 5]],[1, (3, 12), [-3, 5]],[1, (4, 13), [-3, 5]],[1, (5, 7), [-3, 5]],[1, (5, 9), [-3, 5]],[1, (5, 11), [-3, 5]],[1, (8, 12), [-3, 5]],[1, (1, 4), [-2, 4]],[1, (3, 5), [-2, 4]],[1, (4, 6), [-2, 4]],[1, (5, 7), [-2, 4]],[1, (6, 8), [-2, 4]],[1, (8, 10), [-2, 4]],[1, (9, 11), [-2, 4]],[1, (11, 13), [-2, 4]]]
	for [tamanho, posicoes, somas] in lista:
		gerador.addRegra(ValidacaoAnalise.verificarSomasProximaPosicao, anteriores = _sorteios[-tamanho:], posicoes = posicoes, somas = somas)

	print(ultimo.concurso, 'Regras', len(gerador.regras))
	con = gerador.analisarSorteio(ultimo.numeros)
	# gerador.buscarNumerosTeste()
	gerador.calcularReducao(1000)
	gerador.limparRegras()

exit()
# gerador.buscarNumerosTeste()
gerador.calcularReducao(10000)

# tamanho_sorteios = len(sorteios)
# for idx in range(tamanho_sorteios - 12, len(sorteios)):
# 	_sorteios = sorteios[:idx]
# 	analise = Analise(_sorteios)
# 	ultimo = sorteios[idx]

# 	# for comb in list(combinations(range(10), 3)):
# 	# 	ignorar = [(1, 2, 3),(0, 4, 6),(3, 5, 8),(1, 3, 8),(0, 8, 9)]
# 	# 	if len([x for x in ignorar if intersecao(x, comb, True) == len(comb)]) != 0: continue
		
# 	quantidade_anteriores = 3
# 	ret = analise.verificarNumerosxSomas([0,0,0], quantidade_anteriores, 't03')
# 	# pprint.pp(ret)
# 	# break
# 	if ret['lista'][0] < 1:
# 		for (i, x) in enumerate(ret['lista']):
# 			if x < 1:
# 				chaves = list(ret['porcent'].keys())[i]
# 				gerador.addRegra(ValidacaoAnalise.verificarNumerosxSomas, posicoes = [0,0,0], anteriores = _sorteios[-(quantidade_anteriores - 1):], tipo = 't03', evitar = chaves)
# 				contador += 1

# 	print(ultimo.concurso, 'Regras - ', len(gerador.regras))
# 	con = gerador.analisarSorteio(ultimo.numeros)
# 	# gerador.buscarNumerosTeste()
# 	gerador.calcularReducao(1000)
# 	gerador.limparRegras()
# 	# print('-----------', comb)
# 	# break


		

# # def buscarCombos(quantidade, numeros, jogos, numeros_saindo = True, visao_geral = False):
# #     combinacoes = list(combinations(numeros, quantidade))
# #     final = {}
# #     for comb in combinacoes:
# #         chave = '.'.join([str(x) for x in comb])
# #         final[chave] = {'ocorrencias': 0, 'numeros': list(range(26)), 'nunca': list(range(26))}
# #     for n in range(len(jogos)-1):
# #         numeros_jogo = jogos[n].numeros
# #         numeros_proximo_jogo = jogos[n+1].numeros
# #         for comb in combinacoes:
# #             chave = '.'.join([str(x) for x in comb])
# #             if len(intersecao(comb, numeros_jogo)) == len(comb):
# #                 final[chave]['numeros'] = intersecao(final[chave]['numeros'], numeros_proximo_jogo)
# #                 final[chave]['nunca']   = intersecao(final[chave]['nunca'], [x for x in range(1,26) if x not in numeros_proximo_jogo])
# #                 final[chave]['ocorrencias'] = final[chave]['ocorrencias'] + 1
    
# #     if not visao_geral:
# #         final = dict(sorted(final.items(), key=lambda x: x[1]['ocorrencias'], reverse=True))
# #         for chave, valor in final.items():
# #             if len(valor['numeros']) == 1 and numeros_saindo: print(chave, valor)
# #             if len(valor['nunca']) == 1 and (not numeros_saindo): print(chave, valor)
# #     else:
# #         final = dict(sorted(final.items(), key=lambda x: x[1]['ocorrencias'], reverse=False))
# #         for chave, valor in final.items():
# #             print(chave, valor)


# # # Buscar as combinações de números que mais sairam para as dezenas do último jogo
# # buscarCombos(2, ultimo.numeros, sorteios[-20:])
# # print('=====================================')
# # buscarCombos(3, ultimo.numeros, sorteios[-20:])
# # print('-----------------------------------')
# # # Buscar as combinações de números que nunca sairam para as dezenas do último jogo, tem que te pelo menos 5 ocorrências
# # buscarCombos(2, ultimo.numeros, sorteios[-15:], False)
# # print('=====================================')
# # buscarCombos(3, ultimo.numeros, sorteios[-15:], False)

# # exit()

# gerador.addRegraSemArgs(ValidacaoAnalise.analisarCalcularMediaColunas, anteriores = sorteios)

# gerador.calcularReducao(10000)
# gerador.buscarNumerosTeste()

# # exit()


def merge(arr1, arr2):
	novo = []
	for i in range(len(arr2)):
		novo.append(arr1[i])
		novo.append(arr2[i])

	novo.append(arr1[-1])

	return novo

qtd_termos = 4
operacoes = list(permutations(['-', '+', '*', '-', '+', '*', '/', '/'], qtd_termos-1))
# operacoes = list(permutations(operacoes, 2))
ja_tem, op2 = [], []
for op in operacoes:
	# chave = '.'.join(op[0]) + '.'.join(op[1])# + '.'.join(op[2])
	chave = '.'.join(op)
	if ja_tem.count(chave) > 0: continue
	ja_tem.append(chave)
	op2.append(op)

operacoes = op2


termos = []
for i in range(1,10):
	termos.append(str(i) + '*P')
	termos.append('P/' + str(i))

possibilidades = list(permutations(termos, qtd_termos))
ja_tem, op2 = [], []
for op in possibilidades:
	# chave = '.'.join(op[0]) + '.'.join(op[1])# + '.'.join(op[2])
	chave = '.'.join(op)
	if ja_tem.count(chave) > 0: continue
	ja_tem.append(chave)
	op2.append(op)

possibilidades = op2

lista_posicoes = list(combinations(range(15), qtd_termos))

total = len(operacoes) * len(possibilidades) * len(lista_posicoes)

f = open('./txt_temp/extras.txt', 'a')
for op in operacoes:
	for t in possibilidades:
		final = ''.join(merge(t, op))
		verificado_inicio_fim = False
		for pos in lista_posicoes:
			if not verificado_inicio_fim:
				verificado_inicio_fim = True
				qtd_inicio = analise.verificarFuncaoContemNumeroGerado(lista_posicoes[0], final, True)['Qtd Igual']
				qtd_fim = analise.verificarFuncaoContemNumeroGerado(lista_posicoes[-1], final, True)['Qtd Igual']
				if qtd_inicio == qtd_fim and qtd_inicio == 0:
					contador += len(lista_posicoes)
					break
			contador += 1
			if contador < 92000000: continue
			if ''.join(op).endswith('**'): continue
			res = analise.reset().verificarFuncaoContemNumeroGerado(pos, final, True)
			if res['Jogos Analisados'] > 3000 and res['Qtd Igual'] != 0 and (res['Qtd Igual'] < menor or res['Qtd Igual'] > maior):
				if (res['Qtd Igual'] < menor):
					menor = res['Qtd Igual']
				else:
					maior = res['Qtd Igual']
				print('----------------------------------')
				print(res, menor, maior)
				f.write(' '.join([str(res), str(menor), str(maior), str(contador)]))
				f.flush()
			else:
				print(contador, total, final, res['Jogos Analisados'], res['Qtd Igual'], '                                     ', end='\r')