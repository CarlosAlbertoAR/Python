"""
PEP8 - Python Enhancement Proposal

São propostas de melhorias par a linguagem Python

The Zen of Python

import this

A ideia da PEP8 é que possamos escrever códigos Python de forma Pythônica

[1] - Utilize Camel Case para nomes de Classes;

# Certo

class CalculadoraCientifica:
    pass

# Errado

class calculadora_cientifica:
    pass

[2] - Utilize Nomes em minúsculo, separados por underline para funções ou variáveis


# Certo
def soma():
    pass

# Errado
def Soma():
    pass

# Certo

def soma_dois():
    pass

# Errado

def SomaDois():
    pass

# Certo

numero = 4

# Errado
Numero = 4

# Certo

numero_impar = 5

# Errado
NumeroImpar = 5


[3] - Utilize quatro espaços para identação! (Não use tab)

# Errado

if 'a' in 'banana':
print('tem')


# Certo
if 'a' in 'banana':
    print('tem')

[4] - Linhas em branco
- Separar funções e definições de classe com duas linhas em branco;
- Métodos dentro de uma classe devem ser separados com uma única linha em branco;

[5] - Imports
- Imports devem ser sempre feitos em linha separadas;

# Errado
import sys, os

#Certo
import sys
import os

# Não há problemas em utilizar (no máximo 3 objetos)

from types import StringType, ListType;

#Caso tenha muitos imports de um mesmo pacote, recomenda - se

from types import (
    StringType,
    ListType,
    SetType,
    OutroType
)

# Imports devem ser colocados no topo do arquivo, logo depois de quaisquer comentários ou docstrings e
# antes de constantes ou variáveis globais

[6 ] - Espaços em expressões e instruções

# Não faça:

funcao( algo[ 1 ]), { outro: 2 })

# Faça:

função(algo[1]), outro:2})

# Não faça

algo (I)

# Faça:

algo(1)

# Não faça:

dict ['chave'] = lista [indice]

# Faça

dict['chave'] = lista[indice]

# Não faça

x              = 1
y              = 3
variavel_longa = 5

# Faça

x = 1
y = 3
variavel_longa = 5

[7] - Termine sempre uma instrução com uma nova linha

import this

"""



















