import requests

def obter_paises():
    resposta = requests.get('https://restcountries.com/v3.1/all?fields=name,translations')
    dados = resposta.json()
    paises = []
    for pais in dados:
        nome_final = None
        if ('translations' in pais and 
            'por' in pais['translations'] and 
            'common' in pais['translations']['por']):
            nome_final = pais['translations']['por']['common']
        elif 'name' in pais and 'common' in pais['name']:
            nome_final = pais['name']['common']
        if nome_final:
            paises.append(nome_final)
    return sorted(paises)