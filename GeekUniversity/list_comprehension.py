"""
List comprehension

- Utilizando List Comprehension nós podemos gerar novas listas com dados processados a partir de outro iterável

- Sintaxe da List Comprehension

[] Sempre começam por colchetes

[dado for dado in iterável]
"""

# Exemplos

# Utilizando soma dentro da list comprehension
"""
numeros = [1, 2, 3, 4, 5]

res = [numero * 10 for numero in numeros]

print(res)
"""

"""
Para etender melhor o que está acontecendo devemos dividir a expressão em duas partes:

- A primeira parte: for numero in numeros
- A segunda parte: numero * 10
"""

# Utilizando divisão dentro da list comprehension
"""
numeros = [1, 2, 3, 4, 5]

res = [numero / 2 for numero in numeros]

print(res)
"""

# Utilizando uma função dentro da list comprehension
"""
numeros = [1, 2, 3, 4, 5]

def funcao(valor):
    return valor * valor

res = [funcao(numero) for numero in numeros]

print(res)
"""

# Utilizando um loop dentro da list comprehension

# Utilizando loop comumn
"""
numeros = [1, 2, 3, 4, 5]
numeros_dobrados = []

for numero in numeros:
    numero_dobrado = numero * 2
    numeros_dobrados.append(numero_dobrado)

print(numeros_dobrados)
"""

# Utilizando list comprehension
"""
print([numero * 2 for numero in numeros])  # Mostra que você sabe Python avançado
"""

# Utilizando com strings

# Ex 1 - Caixa alta em string
"""
nome = 'Geek University'

print([letra.upper() for letra in nome])
"""

# Ex 2 - Caixa alta em lista de nomes
"""
def caixa_alta(nome):
    nome = nome.replace(nome[0], nome[0].upper())
    return nome


amigos = ['maria', 'julia', 'pedro', 'guilherme', 'vanessa']

print([caixa_alta(amigo) for amigo in amigos])
"""

# Ex 3 - Multiplicação em range
"""
print([numero * 3 for numero in range(1, 10)])
"""

# Ex 4 - conversão de varios dados para boolean
"""
print([bool(valor) for valor in [0, [], '', True, 1, 3.14]])
"""

# Ex 5
"""
print([str(numero) for numero in [1, 2, 3, 4, 5]])
"""

"""
List comprehension - Parte 2

Nós podemos adicionar estruturas condicionais lógicas as nossas List Comprehension
"""

# Exemplo
"""
numeros = [1, 2, 3, 4, 5, 6]

pares = [numero for numero in numeros if numero %2 == 0]
impares = [numero for numero in numeros if numero %2 != 0]

print(pares)
print(impares)
"""

# Refatorando
"""
# Qualquer número par, utilizando o modulo de 2, será 0, e 0 em Python é False
pares = [numero for numero in numeros if not numero % 2]

# Qualquer número ímpar módulo de 2 é 1, e 1 em Python é True
impares = [numero for numero in numeros if numero % 2]

print(pares)
print(impares)
"""

# Outro Exemplo usando else
"""
numeros = [1, 2, 3, 4, 5, 6]
res = [numero * 2 if numero % 2 == 0 else numero / 2 for numero in numeros]
print(res)
"""
