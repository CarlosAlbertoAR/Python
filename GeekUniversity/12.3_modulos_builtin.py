"""
Trabalhando com Módulos Builtin ( Módulos integrados, que já vem instalados no Python

https://docs.pythin.org/3/py-modindex.html

________________________
|Python|Módulos builtin|
"""

# Utilizando alias (apelidos) para módulos/funções
"""
import random as rdm

print(rdm.randint())
"""

# Podemos importar todas as funções de um módulo utilizando um asterítco (*)
# Usando assim não é necessário usar o nome do múdulo antes da função
"""
from random import *

print(randint())
"""

# Importanto todo o módulo, mas tendo que passar a nome do módulo antes da função
""" 
import random

print(random.random())
"""

# Utilizando alias (apelidos) para módulos/funções
"""
from random import randint as rdi, random as rdm

print(rdi(5, 89))

print(rdm())
"""

# Costumamos a utilizar tuple para colocar múltiplos imports de uma mesmo módulo
# Métido mais utilizado
"""
from random import (
    random,
    randint,
    shuffle,
    choice
)

print(random())

print(randint(1, 10))

lista = ['Geek', 'University', 'Python']
shuffle(lista)
print(lista)

print(choice('University'))

"""