"""
Tipo Float

Tipo real, decimal

Casas decimais

Obs: O separador de casas decimais na programação é o ponto e não a virgula
"""

# Errado do ponto de vista do float, mas considera uma tupla

valor = 1, 44
print(valor)
print(type(valor))

# Certo do ponto de vista float
valor = 1.44
print(valor)
print(type(valor))

# É possivel dupla atribuição
valor1, valor2 = 1, 44
print(valor1)
print(type(valor1))
print(valor2)
print(type(valor2))

# Podemos converter um float para um int
# Obs: Ao converter valores float para inteiros, perde-se precisão
res = int(valor)
print(res)
print(type(res))

# Podemos trabalhar com números complexos (representado por "j")
variavel = 5j
print(variavel)
print(type(variavel))





