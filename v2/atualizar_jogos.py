from libs.file_manager import lerSorteados, printCsv
import requests
import json

ultimo = lerSorteados()[-1]
numero_concurso = int(ultimo.concurso) + 1

while True:
    print('buscando', numero_concurso)
    c = requests.get('https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/' + str(numero_concurso), verify=False)

    try:
        dados = c.json()
        if c.status_code != 200: break
    except:
        break

    file = open('../v2/data/temp.json', 'w')

    file.write(json.dumps(dados))

    file.close()

    printCsv()

    numero_concurso += 1
