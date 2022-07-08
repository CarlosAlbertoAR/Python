"""
Listas aninhadas

- Algumas linguagens de programação (C/Java) possuem uma estrutura de dados chamadas de arrays:
    - Unidimensionais (Arrays/Vetores)
    - Multidimensionais (Matrizes)

Em Python nós temos as listas

numeros = [1, 'b', 3.234, True, 5]
"""

listas = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Mariz 3 x 3

# Exemplos
"""
print(listas)

print(type(listas))
"""

# Como fazemos para acessar os dados? Primeiro é zero (0)
"""
print(listas[0][2])  # 2
print(listas[2][1])  # 8
"""

# Interando com loops em uma lista aninhada

# Loop normal
"""
for lista in listas:
    for numero in lista:
        print(numero)
"""

# List Comprehension
"""
[[print(numero) for numero in lista] for lista in listas]
"""

# Outros exemplos

# Gerando um tabuleiro/matrix 3 x 3
"""
tabuleiro = [[numero for numero in range(1, 4)] for valor in range(1, 4)]
print(tabuleiro)
"""

# Gerando jogadas para o jogo da velha (igual exemplo acima, porém com condicional)
"""
velha = [['X' if numero % 2 == 0 else 'O' for numero in range(1, 4)] for valor in range(1, 4)]
print(velha)
"""

# Gerando valores iniciais
"""
print([['*' for i in range(1, 4)] for j in range(1, 4)])
"""
