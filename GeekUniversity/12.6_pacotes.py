"""
Pacotes

Módulo -> É apenas 1 arquivo Python que pode ter diversas funções para utilizarmos.

Pacote -> É um diretório contendo uma coleção de módulos

OBS: Nas versões 2.x do Python, um pacote Python deveria conter dentro dele um arquivo chamado __ini__.py

Nas versões do Python 3.x não é mais obrigatória a utilização deste arquivo, mas normalmente ainda é utilizado para
manter compatibilidade

"""

# Importanto do pacote geek modulos modulo1 e modulo 2

from geek import modulo1, modulo2

print(modulo1.pi)

print(modulo1.funcao1(4, 6))

print(modulo2.curso)

print(modulo2.funcao2())

# Importanto do subpacote university modulos especificos modulo3 e modulo 4

from geek.university import modulo3, modulo4

print(modulo3.funcao3())

print(modulo4.funcao4())

# Importanto do pacote geek modulo modulo1 apenas a função funcão1

from geek.modulo1 import funcao1

print(funcao1(6, 9))

# Importanto do pacote geek subpacote university modulo4 apenas a função funcao4

from geek.university.modulo4 import funcao4

print(funcao4())
