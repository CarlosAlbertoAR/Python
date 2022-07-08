"""
Map

- Map é uma função que recebe 2 parâmetros: O primeiro a função, o sengundo um irterável.
- Retorna um Map Object, podendo ser convertivo para lista, tupla etc

- Ciencia de Dados, Biotecnologia, DataScience, Machine Learning até mesmo porgramação para web

- Com map, fazemos mapeamento de valores para função

- OBS : Após utilizar a função map(), depois da primeira utilização do resultado, ele zera
"""

import math

# Calcular um raio de um circulo depedendo de seu raio

"""
def area(r):
    """"""Calcula a área de um círculo com raio 'r'.""""""
    return math.pi * (r ** 2)


print(area(2))
print(area(5.3))

"""

# E se o caso é uma lista de raios?
raios = [2, 5, 7.1, 0.3, 10, 44]

"""
# Forma comum
areas = []
for r in raios:
    areas.append(area(r))

print(areas)

# Forma 2 - Map

areas = map(area, raios)

print(areas)        # <map object at 0x0352B028>
print(type(areas))  # <class 'map'>
print(list(areas))  # Convertendo para lista

# Forma 3 - Map com Lambda

print(list(map(lambda r: math.pi * (r ** 2), raios)))

"""

# Para fixar - Map

# Temos dados iteráveis:

# dados: a1, a2, ..., an

# Temos uma função:

# Função:

# Função f(x)

# Utilizamos a função map(f, dados) onde Map irá 'mapear' cada elemento dos dados e aplicar a função.

# O Map Object: f(a1), f(a2), f(...), f(an)

# Mais um exemplo
"""
cidades = [('Berlim', 29), ('Cairo', 36), ('Buenos Aires', 19), ('Los Angeles', 26), ('Tókio', 27), ('Nova York', 28)]

print(cidades)

# Conversão de Célsius para Farenheint

# Formula: f = 9/5 * c + 32

# Lambda

c_para_f = lambda dado: (dado[0], (9/5) * dado[1] + 32)

print(list(map(c_para_f, cidades)))
"""