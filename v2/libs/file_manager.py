import csv
import json
from itertools import combinations
from libs.data_process import gerarDicionario
from models.Sorteio import Sorteio
import os.path as pt
import pyperclip

PATH_TODAS_OPCOES = pt.join(pt.abspath(__file__), '..', '..', '..', 'todasOpcoes_01.csv')
PATH_DADOS_BASE = pt.join(pt.abspath(__file__), '..', '..', '..', 'dados_base.csv')
PATH_FILTRO_QUANTIDADE = pt.join(pt.abspath(__file__), '..', '..', 'data', 'todasOpcoesFiltroQuantidade.csv')
PATH_FILTRO_REPETIDOS = pt.join(pt.abspath(__file__), '..', '..', 'data', 'todasOpcoesFiltroRepetidos.csv')
PATH_TEMP = pt.join(pt.abspath(__file__), '..', '..', '..', 'v2', 'data', 'temp.json')

def lerSorteados(quantidade = 0):

    file = open(PATH_DADOS_BASE, 'r', encoding="utf8")

    dados_brutos = csv.reader(file)
    header = next(dados_brutos) # Lê o cabeçalho

    sorteados = []

    for (idx, row) in enumerate(dados_brutos):
        if str(row[0]).upper() == 'FIM': break
        if quantidade > 0 and idx > quantidade -1: break
        sorteados.append(Sorteio(gerarDicionario(row)))

    file.close()
    return sorteados

def gerarCombinacoes(quantidade):
    combinacoes = combinations(list(range(1,26)), quantidade)

    arquivo = open(PATH_TODAS_OPCOES, 'w', newline='')
    writer = csv.writer(arquivo)

    for i,n in enumerate(combinacoes):
        writer.writerow([i,'01/01/2000', *list(n)])

    arquivo.close()

def lerCombinacoes(quantidade = 0):
    
    leitura = open(PATH_TODAS_OPCOES, 'r')
    possibildades_brutas = csv.reader(leitura)
    compilado_possibilidades = []

    for (idx, row) in enumerate(possibildades_brutas):
        if (idx % 100000 == 0): print('Lendo...', idx)
        if (quantidade > 0 and idx > quantidade -1): break
        compilado_possibilidades.append(gerarDicionario(row))

    leitura.close()

    return compilado_possibilidades

def gerarArquivoFiltradoQuantidade():
    leitura = open(PATH_TODAS_OPCOES, 'r')
    arquivo = open(PATH_FILTRO_QUANTIDADE, 'w', newline='')
    writer = csv.writer(arquivo)

    possibildades_brutas = csv.reader(leitura)
    rows = 0

    for (idx, row) in enumerate(possibildades_brutas):
        x = gerarDicionario(row)
        if (idx % 100000 == 0): print(idx, rows)
        
        if not (x['quantidade_col_1'] < 1
            or x['quantidade_col_2'] < 1
            or x['quantidade_col_3'] < 1
            or x['quantidade_col_4'] < 1
            or x['quantidade_col_5'] < 1
            or x['numeros'][0] > 3
            or x['numeros'][1] > 6
            or x['numeros'][2] > 8
            or x['numeros'][3] > 10
            or x['numeros'][4] > 11
            or x['numeros'][5] > 13
            or x['numeros'][6] < 8 or x['numeros'][6] > 14
            or x['numeros'][7] < 10 or x['numeros'][7] > 16
            or x['numeros'][8] < 11 or x['numeros'][8] > 18
            or x['numeros'][9] < 13 or x['numeros'][9] > 19
            or x['numeros'][10] < 15 
            or x['numeros'][11] < 17 
            or x['numeros'][12] < 19 
            or x['numeros'][13] < 20 
            or x['numeros'][14] < 23 
            or x['soma'] > 225 or x['soma'] < 156
			or x['pares'] < 5 or x['pares'] > 9
			or x['impares'] < 6 or x['impares'] > 10
			or x['maior_sequencia'] < 3 or x['maior_sequencia'] > 8
			or x['quantidade_sequencias'] < 1 or x['quantidade_sequencias'] > 4
			or x['quantidade_menores_10'] < 3 or x['quantidade_menores_10'] > 8
			or x['quantidade_entre_10_20'] < 4 or x['quantidade_entre_10_20'] > 8
			or x['quantidade_maiores_20'] < 1
			or x['quantidade_primos'] < 3 or x['quantidade_primos'] > 8
			or x['diferenca_maxima'] > 7  or x['diferenca_maxima'] == 1
			or x['quantidade_menores_13'] < 5 or x['quantidade_menores_13'] > 10
			or x['quantidade_maiores_13'] < 4 or x['quantidade_maiores_13'] > 9
			or x['quantidade_meio'] < 2 or x['quantidade_meio'] > 8
        ):    
            writer.writerow([x['concurso'],'01/01/2000', *list(x['numeros'])])
            rows = rows + 1

        

    leitura.close()
    arquivo.close()
    print('Fim')


def printCsv():
    
    file = open(PATH_TEMP, 'r', encoding="utf8")

    dados_brutos = json.load(file)
    
    print(str(dados_brutos['numero']) + ',' + dados_brutos['dataApuracao'] + ','.join(list(map(lambda x: str(int(x)), dados_brutos['listaDezenas']))) + ',0')

    file_base = open(PATH_DADOS_BASE, 'a')
    file_base.write("\n" + str(dados_brutos['numero']) + ',' + dados_brutos['dataApuracao'] + ',' + ','.join(list(map(lambda x: str(int(x)), dados_brutos['listaDezenas']))) + ',0')
    file_base.close()

    pyperclip.copy(str(dados_brutos['numero']) + ',' + dados_brutos['dataApuracao'] + ',' + ','.join(list(map(lambda x: str(int(x)), dados_brutos['listaDezenas']))) + ',0')
    file.close()
    print('Fim da leitura')
    # return possiveis?