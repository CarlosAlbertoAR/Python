"""
Módulo Collections - Named Tuple

https://docs.python.org/3/library/collections.html#collections.namedtuple

Named Tuple -> São tuplas diferenciadas, onde especificamos um nome para a mesma e tambpém parâmetros.
"""

# Importando

from collections import namedtuple

"""
tupla = (1, 2, 3)

print(tuple[1])
"""

# Precisamos definir o nome e parâmetros

# Forma 1 - Declaração Named Tuple

cachorro = namedtuple('cachorro', 'idade raca nome')

# Forma 2 - Declaração Named Tuple

cachorro = namedtuple('cachorro', 'idade, raca, nome')

# Forma 3 - Declaração Named Tuple

cachorro = namedtuple('cachorro', ['idade', 'raca', 'nome'])  # Forma preferível

# Usando

ray = cachorro(idade=2, raca='Chow Chow', nome='Ray')
print(ray)
print(type(ray))

# Acessando os dados

# Forma 1

print(ray[0])  # idade
print(ray[1])  # raca
print(ray[2])  # nome

# Forma 2

print(ray.idade)  # idade
print(ray.raca)  # raca
print(ray.nome)  # nome

print(ray.index('Chow Chow'))  # Pesquisando qual é o indice

print(ray.count('Chow Chow'))  # Contagem de ocorrências
