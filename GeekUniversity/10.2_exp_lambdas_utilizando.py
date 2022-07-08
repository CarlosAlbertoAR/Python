"""
Expressões lambdas

Conhecidas por Exmpressões Lambdas, ou simplesmente Lambdas, são funções sem nome, ou seja, funções anônimas.

Geralmente usadas em filtragem e ordenação de dados, mas não se limitando a isto

- Quem domina Comprehensions e Lambdas está em nível avançado de Python

"""

# Declaração e uso
"""
# Função em Python

def funcao(x):
    return 3 * x + 1

print(funcao(4))

# Expressão Lambda

lambda x: 3 * x + 1

# E como utilizar a expressão lambda?

calc = lambda x: 3 * x + 1

print(calc(4))
"""

# Podemos ter expressões lambdas com múltimas entradas
"""
nome_completo = lambda nome, sobrenome: nome.strip().title() + ' ' + sobrenome.strip().title()

print(nome_completo(' angelina', 'JOLIE'))
print(nome_completo('   FELICITY      ', ' jones  '))
"""

# Em funções Python podemos ter nenhuma ou várias entradas. Em Lambdas também
"""
amar = lambda: 'Como não amar Python?'

uma = lambda x: 3 * x + 1

duas = lambda x, y: (x * y) ** 0.5

tres = lambda x, y, z: 3 / (1 / x + 1 / y + 1 / z)

# n = lambda x1, x1, ..., xn: <expressão>

print(amar())
print(uma(6))
print(duas(5, 7))
print(tres(3, 6, 9))

# OBS: Se passarmos mais argumentos do que parâmetros, teremos um TypeError, como uma função def
"""

# Ordenando pelo sobrenome usando expressão lambda
"""
autores = ['Isaac Asimov', 'Ray Bradbury', 'Robert Heinlein', 'Arthur C. Clarque', 'Frank Herbert',
           'Orson Scott Card', 'Douglas Adms', 'H. G. Wells', 'Leigh Brackett']

print(autores)

autores.sort(key=lambda sobrenome: sobrenome.split(' ')[-1].lower())

print(autores)
"""

# Função Quadrática
# f(x) = a * x ** 2 + b * x + c

# Definindo a função, recebe 3 parametros e tem como retorno uma lambda com um parametro (x)
"""
def geradora_funcao_quadratica(a, b, c):
    """""" Retorna a função f(x) = a * x ** 2 + b * x + c """"""
    return lambda x: a * x ** 2 + b * x + c


teste = geradora_funcao_quadratica(2, 3, -5)

print(teste(0))
print(teste(1))

# Ou

print(geradora_funcao_quadratica(3, 0, 1)(2))
"""
