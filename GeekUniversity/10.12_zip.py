"""
Zip

zip() cria um iterável chamado (Zip Object) que agrega elemento de cada um dos iteráveis passado com entrada em pares.
"""

lista1 = [1, 2, 3]
lista2 = [4, 5, 6]

zip1 = zip(lista1, lista2)

print(zip1)
print(type(zip1))  # <class 'zip'>

# Sempre podemos gerar uma lista, Tupla, ou Dicionário
# Assim como no map, filter, generetor ele é trabalhado é eliminado da memória

print(list(zip1))  # [(1, 4), (2, 5), (3, 6)]

zip1 = zip(lista1, lista2)
print(tuple(zip1))  # ((1, 4), (2, 5), (3, 6))

zip1 = zip(lista1, lista2)
print(set(zip1))  # {(2, 5), (1, 4), (3, 6)}

zip1 = zip(lista1, lista2)
print(dict(zip1))  # {1: 4, 2: 5, 3: 6}


# Listas de tamanhos diferentes
# Para mediante o tamanho da menor lista
"""
lista3 = [7, 8, 9, 10, 11]

zip1 = zip(lista1, lista2, lista3)
print(list(zip1))  # [(1, 4, 7), (2, 5, 8), (3, 6, 9)] 
"""

# Podemos utilizar diferentes iteráveis com zip
"""
tupla = 1, 2, 3, 4, 5
lista = [6, 7, 8, 9, 10]
dicionario = {'a': 11, 'b': 12, 'c': 13, 'd': 14, 'e': 15}

zt = zip(tupla, lista, dicionario.values())
print(list(zt))
"""

# Lista de Tuplas
"""
dados = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]

print(list(zip(*dados)))  # [(0, 1, 2, 3, 4), (1, 2, 3, 4, 5)] * desempacota, primeiro de cada, depois segundo de cada
"""

# Exemplos mais complexos
"""
prova1 = [80, 91, 78]
prova2 = [98, 89, 53]
alunos = ['maria', 'pedro', 'carla']
"""
"""
No exemplo abaixo, para cada dado, resultado do zip, passe a primeiro posição (nome) como chave, e maior entre as notas
(nota 1 e nota 2) como valor
"""
"""
final = {dado[0]: max(dado[1], dado[2]) for dado in zip(alunos, prova1, prova2)}
print(final)
"""

# Podemos utilizar o map()

"""
No exemplo abaixo, da direita para esquerda, cria uma lista com tuplas de notas, passa cada tupla para a lambda 
que retorna o max() de cada, o zip entre a lista de alunos e o resultado da lambda  
"""
"""
final = zip(alunos, map(lambda nota: max(nota), zip(prova1, prova2)))
print(dict(final))
"""