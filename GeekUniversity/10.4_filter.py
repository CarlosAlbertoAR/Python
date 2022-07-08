"""
Filter

- Serve para filtras dados de uma determinada coleção.

- OBS : Assim como a função map(), a filter recebe 2 parâmetros, sendo uma função e um iterável

- o Retorno é um "filter object"

- Assim como o map, após ser utilizada a primeira vez, zera

- Diferença entre map e filter:
    map() recebe dois parâmetros, uma função e um interável e retorna um objeto mapeando a função para casa elemento do
    iterável, a função de entrada retorna valores quaisquer

    filter() recebe dois parÂmetros, uma função e um iterável e retorna um objeto filtrando apenas os elementos de
    acordo com a condição informada, , a função de entrada apenas true ou false, fazendo com que os dados seja filtrado
    ou não


"""

import statistics

# Média do método normal
""" 
valores = 1, 2, 3, 4, 5, 6

media = sum(valores) / len(valores)

print(media)
"""

# Dados coletados de algum sensor
"""
dados = [1.3, 2.7, 0.8, 4.1, 4.3, -0.1]

# Calculando a média dos dados utilizando a função mean()
media = statistics.mean(dados)
print(f'Média: {media}')

res = filter(lambda x: x > media, dados)
print(list(res))

print(f'Novamente: {list(res)}')  # Zerado
"""

# Remoção de dados faltantes

"""
paises = ['', 'Argentina', '', 'Brasil', 'Chile', 'Colombia', '', 'Equador', '', '', 'Venezuela']

print(paises)
"""

"""
# 1º Forma com lambda
res = filter(lambda pais: len(pais) > 0, paises)

print(list(res))
"""

"""
# 2º Forma com lambda
res = filter(lambda pais: pais != '', paises)

print(list(res))
"""

"""
# Forma inteligente com None
res = filter(None, paises)

print(list(res))
"""

# Exemplo mais complexo
"""
usuarios = [
    {"username": "samuel", "tweets": ["Eu adoro bolos", "Eu Adoro pizzas"]},
    {"username": "carla", "tweets": ["Eu amo meus gato"]},
    {"username": "jeff", "tweets": []},
    {"username": "bob", "tweets": []},
    {"username": "doggo", "tweets": ["Eu gosto de cachorros", "Vou sair hoje"]},
    {"username": "gal", "tweets": []}
]

print(usuarios)

# Filtrar os usuários que estão inativos no Twitter

# Forma 1 - Testanto o numero de tweets
inativos = list(filter(lambda usuario: len(usuario['tweets']) == 0, usuarios))

# Forma 2 - Lista vazia convertida em boolean é = False
inativos = list(filter(lambda usuario: not usuario['tweets'], usuarios))

print(inativos)
"""

# Combinar filter() e map ()
"""
nomes = ['Vanessa', 'Ana', 'Maria']

# Devemos criar uma lista contendo 'Sua instrutora é' + nome, desde que cada nome tenha menos de 5 caracteres

lista = list(map(lambda nome: f'Sua instrutora é {nome}', filter(lambda nome: len(nome) < 5, nomes)))

print(lista)
"""


