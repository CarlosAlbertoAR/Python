"""
Reversed

OBS: Não confunda com a função reverse() que estudamos nas listas.

A função reverse() só funciona em listas.

Já a função reversed() funciona com qualquer iterável.

Sua função é inverter o iterável.

A função reversed() retorna um iterável chamado List Reverse Interator

"""

# Exemplos
#
"""
lista = [1, 2, 3, 4, 5]

res = reversed(lista)

print(res)
print(type(res))
"""

# Pode ser convertida oara uma lista, Tupla ou Conjunto
"""
# Lista
print(list(reversed(lista)))

# Tupla
print(tuple(reversed(lista)))

# Set OBS : Set não define ordem
print(set(reversed(lista)))

# Podemos iterar sobre o reversed
for letra in reversed('Geek University'):
    print(letra, end='')  # end='' para não saltar linha
"""

# Podemos fazero mesmo sem o uso do for
"""
print('\n')
print(''.join(list(reversed('Geek University'))))
"""

# Já vimos como fazer isso mais fácil com slice de strings
"""
print('Geek University'[::-1])
"""

# Podemos também utilizar o reversed() para fazer um loop for reverso
"""
for n in reversed(range(0, 10)):
    print(n)
"""

# Apesar que também ja vimos como fazer issto utilizando o próprio range()
"""
for n in (range(10, -1, -1)):
    print(n)
"""

