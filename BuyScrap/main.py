
import pandas as pd  # Estatísticas e grandes volumes de dados
import numpy as np
import requests  # REquisição HTTP
from bs4 import BeautifulSoup  # Transformar os dados da request como html
import json
from difflib import SequenceMatcher
from selenium import webdriver  # Automatização do navegador
import time
from datetime import date
import re  # regex para campos em strings

class OLXCategoriaError(Exception):
    pass


def buscarDadosOLX(regiao, categoria, pages = 2):
    # https://[UF].olx.com.br/[REGIAO]/[CATEGORIA]
    listaRegiao = {'GO62': 'grande-goiania-e-anapolis', 'GO64': 'regiao-de-rio-verde-e-caldas-novas'}
    listaCategoria = ('imoveis', 'autos-e-pecas', 'para-a-sua-casa', 'eletronicos-e-celulares', 'musica-e-hobbies',
                      'esportes-e-lazer', 'artigos-infantis', 'animais-de-estimacao', 'moda-e-beleza',
                      'agro-e-industria', 'comercio-e-escritorio', 'servicos', 'vagas-de-emprego')

    if not categoria in listaCategoria:
        print(f'Categoria não suportada: {categoria}')
        pass

    dominio = f'{regiao[:2].lower()}.olx.com.br'

    for x in range(0, pages):
        print(f'BUSCANDO OLX. PÁG {str(x)}')
        page = ''
        if x > 0:
            page = f'?o={str(x)}'
        url = f'https://{dominio}/{listaRegiao[regiao]}/{categoria}{page}'
        print(url)

        params = {"authority": f'"{dominio}"',
                  "method": "GET",
                  "path": f'"/{listaRegiao[regiao]}/{categoria}"',
                  "scheme": "https",
                  "referer": f'"{url}"',
                  "sec-fetch-mode": "navigate",
                  "sec-fetch-site": "same-origin",
                  "sec-fetch-user": "?1",
                  "upgrade-insecure-requests": "1",
                  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
                  }

        # Requisita e retorna html
        page = requests.get(url=url, headers=params)
        soup = BeautifulSoup(page.content, 'lxml')
        # Separa apenas classes dos anúncios
        itens = soup.find_all('li', {'class' : 'sc-1fcmfeb-2 juiJqh'})
        print(len(itens))

        # Lista os nomes dos anuncios, está no h2
        for a in itens:
            try:
                nomeAnuncio = a.find_all('h2')[0].contents[0]
                valorAnuncio = sc-ifAKCX eoKYee
            except:
                print('Erro ao obter nome.')

buscarDadosOLX('GO62', 'imoveis', pages=2)
