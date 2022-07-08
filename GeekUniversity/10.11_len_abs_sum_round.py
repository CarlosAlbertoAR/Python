"""
Len, Abs, Sum, Round

# len() - Retorna o tamanho (ou seja, o número de itens) de um iterável)
"""

# Apenas para revisar
"""
print(len('Geek University'))

print(len([1, 2, 3, 4, 5]))  # 15

print(len((1, 2, 3, 4, 5)))  # 5

print(len({1, 2, 3, 4, 5}))  # 5

print(len({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}))  # 5

print(len(range(0, 10)))  # 10
"""

# Por debaixo dos panos, quando utilizados a função len() o Pyhton faz o seguinte:

# Dunder len
"""
print('Geek University'.__len__())
"""
# abs() - Retorna o valor absulotu de um número inteiro ou real. De forma básica, seria o seu valor real sem o sinal.
"""
print(abs(-5))
print(abs(5))
print(abs(3.14))
print(abs(-3.14))
"""

# sum() - Retorna como parâmetro o iterável, podendo receber um valor inicial, e retorna a soma total dos elementos,
# incluindo o valor inicial

# OBS: O valor inicial default = 0

# Exemplos Sum
"""
print(sum([1, 2, 3, 4, 5]))

print(sum([1, 2, 3, 4, 5], 5))

print(sum([3.145, 5.678]))

print(sum((1, 2, 3, 4, 5)))

print(sum({1, 2, 3, 4, 5}))

print(sum({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}.values()))
"""

# Round
# round() - Retorna um número arredondado para o digito de precisão após a casa decimal. Se a precisão não for informada
# retorna o inteiro mais próximo da entrada

# Exemplos
"""
print(round(10.2))  # 10

print(round(10.5))  # 10

print(10.6)  # 10.6

print(round(1.21212121212, 2))  # 1.21

print(round(1.219999999, 2))  # 1.22

print(round(1.21212121212))  # 1
"""
