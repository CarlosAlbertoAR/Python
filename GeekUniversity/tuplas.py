"""
Tuplas (tuple)

Tuplas são bastante parecidas com listas.

Existem basicamente 2 diferenças basicas:

1 - As Tuplas são representadas por parênteses ()

2 - As tuplas são imotáveis: Isso significa que ao se criar uma tupla ela não muda. Toda alteração em uma
tupla, gera uma nova tupla.

"""

# CUIDADO 1 : As Tuplas são representadas por (), mas veja:
"""
tupla1 = (1, 2, 3, 4, 5, 6)
print(tupla1)
print(type(tupla1))

tupla2 = 1, 2, 3, 4, 5, 6  # Mesmo sem parntese
print(tupla2)
print(type(tupla2))
"""
# CUIDADO 2 : Tuplas com 1 elemento
"""
tupla3 = (4)  # Isso não é uma tupla!
print(tupla3)
print(type(tupla3))

tupla4 = (4,)  # Isso sim é uma tupla!
print(tupla4)
print(type(tupla4))

tupla5 = 4,
print(tupla5)
print(type(tupla5))

# CONCLUSÃO: Podemos concluir que tuplas são definidas pela vírgula e não pelo uso do parênteses

(4) Não é tupla
(4,) É tupla
4, É tupla
"""

# Podemos gerar uma tupla dinamicamente com range(inicio, fim, passo)
"""
tupla = tuple(range(11))
print(tupla)
print(type(tupla))
"""

# Desempacotamento de tupla
# Obs: O números de variaveis e elementos devem ser iguais, caso contrário surge um ValueError
"""
tupla = ('Geek University', 'Programação em Python: Essencial')
print(tupla)

escola, curso = tupla

print(escola)
print(curso)
"""

# Métodos para adição e remoção de elementos nas tuplas não existem, dado o fato da tuplas serem imutaveis.

# Soma*, Valor Máximo*, Valor Mínimo* e tamanho
# * Se os valores forem todos inteiros ou reais
"""
tupla = (1, 2, 3, 4, 5, 6)

print(sum(tupla)) 
print(min(tupla))
print(max(tupla))
print(len(tupla))
"""

# Concatenação de tuplas
"""
tupla1 = (1, 2, 3)
print(tupla1)

tupla2 = (4, 5, 6)
print(tupla2)

print(tupla1 + tupla2)

print(tupla1)
print(tupla2)

tupla3 = tupla1 + tupla2  # Criando novo com a concatenação dos valores
print(tupla3)

tupla1 = tupla1 + tupla2  # São imutaveis mas podemos sobreescrever seus valores
"""

# Verificar se determinado elemento está contido na tupla
"""
tupla = (1, 2, 3)
print(3 in tupla)
"""
# Iterando sobre uma tupla
"""
tupla = (1, 2, 3)

for n in tupla:
    print(n)

for indice, valor in enumerate(tupla):
    print(indice, valor)
"""
# Cotando elementos dentro de uma tupla
"""
tupla = ('a', 'b', 'c', 'd', 'e', 'a', 'b')

print(tupla.count('a'))

escola = tuple('Geek University')
print(escola)
print(escola.count('e'))
"""
# Dicas na utilização de tuplas

# Devemos utilizar tuplas SEMPRE que não precisarmos modificas os dados contidos em uma coleção

# Exemplo 1

meses = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outrubro', 'Novembro', 'Dezembro')

# O acesso de elementos de uma tupla também é semelhante a de uma lista
"""
print(meses[5])
"""
# Iterar com while
"""
i = 0

while i < len(meses):
    print(meses[i])
    i += 1
"""
# Verificarmos em qual índice um elemento está na tupla
"""
print(meses.index('Maio'))
print(meses.index('Maio', 2))
"""
# Slicing

# tupla[inicio:fim:passo
"""
print(meses[0:])  # Todos
print(meses[5:])  # A partir de Junho
"""
# Porque utilizar tuplas?

# - Tuplas são mais rápidas do que listas.

# - Tuplas deixam seu código mais seguro*.

# * Trabalhar com elementos imutáveis traz segurança para o código

# Copiando uma tupla para outra

original = (1, 2, 3)
print(original)

nova = original  # Na tupla não temos o problema de Shallow Copy

print(original)
print(nova)

outra = (4, 5, 6)

nova = nova + outra

print(nova)
print(original)
