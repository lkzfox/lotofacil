import datetime as dt
from  libs.helper import *
import pprint
from itertools import combinations
from models.Sorteio import *

def gerarDicionario(row, tamanho = 15):
    inverso = row[1].split('/')
    inverso.reverse()
    numeros = list(map(lambda x: int(x), row[2:2+tamanho]))
    pares = [x for x in numeros if x % 2 == 0]
    impares = [x for x in numeros if x % 2 != 0]

    multiplicacao = 1
    for n in numeros:
        multiplicacao *= n

    dict_temp = {
        'concurso': int(row[0]),
        'dia_semana': dt.date(*map(lambda x: int(x), inverso)).weekday(),
        'numeros': numeros,
        'numeros_nao': [x for x in range(1,26) if x not in numeros],
        'soma': sum(numeros),
        'soma_maior_media': sum(numeros) > 195,
        'multiplicacao': multiplicacao,
        'pares': len(pares),
        'pares_maior_media': len(pares) > 6,
        'soma_pares': sum(pares),
        'impares': len(impares),
        'soma_impares': sum(impares),
        'quantidade_grupo_5': quantidadeGrupo(numeros, 5),
        'quantidade_grupo_3': quantidadeGrupo(numeros, 3),
        'maior_sequencia': maxSequencia(numeros),
        'quantidade_sequencias': qtdSequencias(numeros),
        'quantidade_menores_6': len([x for x in numeros if x < 6]),
        'soma_menores_6': sum([x for x in numeros if x < 6]),
        'quantidade_menores_12': len([x for x in numeros if x < 12]),
        'soma_menores_12': sum([x for x in numeros if x < 12]),
        'quantidade_menores_18': len([x for x in numeros if x < 18]),
        'soma_menores_18': sum([x for x in numeros if x < 18]),		
        'quantidade_entre_5_10': len([x for x in numeros if x >= 5 and x < 10]),
        'soma_entre_5_10': sum([x for x in numeros if x >= 5 and x < 10]),
        'quantidade_entre_10_15': len([x for x in numeros if x >= 10 and x < 15]),
        'soma_entre_10_15': sum([x for x in numeros if x >= 10 and x < 15]),
        'quantidade_entre_15_20': len([x for x in numeros if x >= 15 and x < 20]),
        'soma_entre_15_20': sum([x for x in numeros if x >= 15 and x < 20]),
        'quantidade_menores_10': len([x for x in numeros if x < 10]),
        'soma_menores_10': sum([x for x in numeros if x < 10]),
        'quantidade_entre_10_20': len([x for x in numeros if x >= 10 and x < 20]),
        'soma_entre_10_20': sum([x for x in numeros if x >= 10 and x < 20]),
        'quantidade_maiores_20': len([x for x in numeros if x >= 20]),
        'soma_maiores_20': sum([x for x in numeros if x >= 20]),
        'quantidade_primos': len([x for x in numeros if x in [2,3,5,7,11,13,17,19,23]]),
        'soma_primos': sum([x for x in numeros if x in [2,3,5,7,11,13,17,19,23]]),
        'primos_maior_media': len([x for x in numeros if x in [2,3,5,7,11,13,17,19,23]]) > 5,
        'diferenca_maxima': maxDiferencaVizinhos(numeros),
        'quantidade_menores_13': len([x for x in numeros if x < 13]),
        'soma_menores_13': sum([x for x in numeros if x < 13]),
        'quantidade_maiores_13': len([x for x in numeros if x > 13]),
        'soma_maiores_13': sum([x for x in numeros if x > 13]),
        'quantidade_meio': len(intersecao([7,8,9,12,13,14,17,18,19], numeros)),
        'soma_meio': sum(intersecao([7,8,9,12,13,14,17,18,19], numeros)),
        'quantidade_col_1': len(intersecao(list(range(1, 26, 5)), numeros)),
        'soma_col_1': sum(intersecao(list(range(1, 26, 5)), numeros)),
        'quantidade_col_2': len(intersecao(list(range(2, 26, 5)), numeros)),
        'soma_col_2': sum(intersecao(list(range(2, 26, 5)), numeros)),
        'quantidade_col_3': len(intersecao(list(range(3, 26, 5)), numeros)),
        'soma_col_3': sum(intersecao(list(range(3, 26, 5)), numeros)),
        'quantidade_col_4': len(intersecao(list(range(4, 26, 5)), numeros)),
        'soma_col_4': sum(intersecao(list(range(4, 26, 5)), numeros)),
        'quantidade_col_5': len(intersecao(list(range(5, 26, 5)), numeros)),
        'soma_col_5': sum(intersecao(list(range(5, 26, 5)), numeros)),
        'quantidade_pares_pos_a': len([x for (i, x) in enumerate(numeros) if x % 2 == 0 and i in [0,1,3,4,7,9]]),
        'soma_pares_pos_a': sum([x for (i, x) in enumerate(numeros) if x % 2 == 0 and i in [0,1,3,4,7,9]]),
        'quantidade_pares_pos_b': len([x for (i, x) in enumerate(numeros) if x % 2 == 0 and i in [0,4,7,9,11,12]]),
        'soma_pares_pos_b': sum([x for (i, x) in enumerate(numeros) if x % 2 == 0 and i in [0,4,7,9,11,12]]),
        'quantidade_pares_pos_c': len([x for (i, x) in enumerate(numeros) if x % 2 == 0 and i in [0,1,9,10,13,14]]),
        'soma_pares_pos_c': sum([x for (i, x) in enumerate(numeros) if x % 2 == 0 and i in [0,1,9,10,13,14]]),
        'quantidade_pares_pos_d': len([x for (i, x) in enumerate(numeros) if x % 2 == 0 and i in [0,1,3,4,7,9,10,12]]),
        'soma_pares_pos_d': sum([x for (i, x) in enumerate(numeros) if x % 2 == 0 and i in [0,1,3,4,7,9,10,12]]),
        'quantidade_pares_pos_e': len([x for (i, x) in enumerate(numeros) if x % 2 == 0 and i in [0,4,7,9,11,12,13,14]]),
        'soma_pares_pos_e': sum([x for (i, x) in enumerate(numeros) if x % 2 == 0 and i in [0,4,7,9,11,12,13,14]]),
        'quantidade_pares_pos_f': len([x for (i, x) in enumerate(numeros) if x % 2 == 0 and i in [0,1,5,6,9,10,13,14]]),
        'soma_pares_pos_f': sum([x for (i, x) in enumerate(numeros) if x % 2 == 0 and i in [0,1,5,6,9,10,13,14]]),
    }

    return dict_temp


def gerarDicionarioSimples(numeros):
    return gerarDicionario(['0', '01/01/2000', *numeros, 0], len(numeros))

def gerarSorteioSimples(numeros):
    return Sorteio(gerarDicionario(['0', '01/01/2000', *numeros, 0], len(numeros)))
