"""
Módulo Collections: Ordered Dict

https://docs.python.org/3/library/collections.html#collections.OrderedDict

Ordered Dict é um dicionário que nos garante o retorno na ordem de inserção dos elementos.
"""
# Em um dicionário, a ordem de inserção dos elementos não é garantida.
"""
dicionario = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
print(dicionario)
"""

# Fazendo o import
from collections import OrderedDict

dicionario = OrderedDict({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})
"""
for chave, valor in dicionario.items():
    print(f'chave={chave}:valor{valor}')
"""
# Entendendo a difrença entre Dict e ordered Dict

# Dicionários comuns

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 2, 'a': 1}

print(dict1 == dict2)  # True, ja que a ordem dos elementos não importa para o dicionário

# Ordered Dict

odict1 = OrderedDict({'a': 1, 'b': 2})
odict2 = OrderedDict({'b': 2, 'a': 1})

print(odict1 == odict2)  # False, ja que a ordem de inserção dos elementos importa para o OrderedDict
