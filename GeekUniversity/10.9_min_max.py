"""
Min e Max

- Funcionam para qualquer iterável, listam, tupla, set

max() - Retorna o maior valor em um iterável ou maior dos dois ou mais elementos

min() - Retorna o menor valor em um iterável ou o menor de dois ou o mais elementos

"""

# Exemplos max()
"""
lista = [1, 8, 4, 99, 34, 129]
print(max(lista))  # 129

tupla = (1, 8, 4, 99, 34, 129)
print(max(tupla))  # 129

conjunto = {1, 8, 4, 99, 34, 129}
print(max(conjunto))  # 129

dicionario = {'a': 1, 'b': 8, 'c': 4, 'd': 99, 'e': 34, 'f': 129}
print(max(dicionario))  # f

dicionario = {'a': 1, 'b': 8, 'c': 4, 'd': 99, 'e': 34, 'f': 129}
print(max(dicionario.values()))  # 129
"""

# Faça um programa que receba dois valores do usuário e mostre o maior
"""
val1 = int(input('Informe o primeiro valor: '))
val2 = int(input('Informe o segundo valor: '))

print(f'O maior valor é: {max(val1, val2)}')
"""

"""
print(max(4, 67, 54))  # 67

print(max('a', 'ab', 'abc'))  # abc

print(max('a', 'b', 'c', 'g'))  # g

print(max(3.145, 5.789))  # 5.789

print(max('Geek University'))  # y (mais no final do alfabeto)
"""

# Exemplos min()
"""
lista = [1, 8, 4, 99, 34, 129]
print(min(lista))  # 1

tupla = (1, 8, 4, 99, 34, 129)
print(min(tupla))  # 1

conjunto = {1, 8, 4, 99, 34, 129}
print(min(conjunto))  # 1

dicionario = {'a': 1, 'b': 8, 'c': 4, 'd': 99, 'e': 34, 'f': 129}
print(min(dicionario))  # a

dicionario = {'a': 1, 'b': 8, 'c': 4, 'd': 99, 'e': 34, 'f': 129}
print(min(dicionario.values()))  # 1
"""

# Faça um programa que receba dois valores do usuário e mostre o maior
"""
val1 = int(input('Informe o primeiro valor: '))
val2 = int(input('Informe o segundo valor: '))
"""
"""
print(f'O maior valor é: {min(val1, val2)}')

print(min(4, 67, 54))  # 4

print(min('a', 'ab', 'abc'))  # a

print(min('a', 'b', 'c', 'g'))  # a

print(min(3.145, 5.789))  # 3.145

print(min('Geek University'))  # y (mais no final do alfabeto)
"""

# Exemplos mais complexos
"""
nomes = ['Arya', 'Samson', 'Dora', 'Tim', 'Olivander']

print(max(nomes))  # Tim (levando em consideração a ordem no alfabeto)

print(min(nomes))  # Arya (levando em consideração a ordem no alfabeto)

print(max(nomes, key=lambda nome: len(nome)))  # Ollivanxer

print(min(nomes, key=lambda nome: len(nome)))  # Tim
"""

musicas = [
    {"titulo": "Thunderstruck", "tocou": 3},
    {"titulo": "Dead Skin Mask", "tocou": 2},
    {"titulo": "Back in Black", "tocou": 4},
    {"titulo": "Too old to rock'in'roll", "tocou": 32}
]

# Pra cada música, retorne a chave 'tocou', sendo o resultante da função passada como parametros de max e min
print(max(musicas, key=lambda musica: musica['tocou']))
print(min(musicas, key=lambda musica: musica['tocou']))

# DESAFIO! Imprima somente o título da música mais e menos tocada

print(max(musicas, key=lambda musica: musica['tocou'])['titulo'])
print(min(musicas, key=lambda musica: musica['tocou'])['titulo'])

# DASAFIO! Sem utilizar nem o max, min, e sem lambda

# max
max = 0
for musica in musicas:
    if musica['tocou'] > max:
        max = musica['tocou']

for musica in musicas:
    if musica['tocou'] > max:
        print(musica['titulo'])


# min
min = 99999
for musica in musicas:
    if musica['tocou'] > min:
        max = musica['tocou']

for musica in musicas:
    if musica['tocou'] == min:
        print(musica['titulo'])