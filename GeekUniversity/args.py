"""
Entendendo o *args

- O *args é um parâmetro, como um outro qualquer. Isso significa que você poderá chamar de qualquer coisa, desde que
começe com asteristico.

Exemplo:

*xis

Mas por ocnvenção, utilizamos *args para definí-lo

Mas o que é *args?

O parâmetro *args utilizando em uma função, coloca os valores extras informados como entrada em uma tupla.
Então desde já lembre-se que tuplas são imutáveis
"""

# Exemplos
"""

def soma_todos_numeros(num1, num2, num3):
    return num1 + num2 + num3


print(soma_todos_numeros(4, 6, 9))

# print(soma_todos_numeros(4, 6))  # TypeError

# print(soma_todos_numeros(4, 6, 9, 5))  # TypeError

print(soma_todos_numeros(4, 6, 9))
"""

# Com args
"""

def soma_todos_numeros(*args):
    return sum(args)

print(soma_todos_numeros())
print(soma_todos_numeros(1))
print(soma_todos_numeros(1, 2))
print(soma_todos_numeros(1, 2, 3))
print(soma_todos_numeros(1, 2, 3, 4))


# args com outros parametros

def soma_todos_numeros(nome, sobrenome, *args):
    return sum(args)

print(soma_todos_numeros('Geek', 'University', 4, 5, 6 ))
"""

# Outro exemplo de utilização do *args
"""

def verifica_info(*args):
    if 'Geek' in args and 'University' in args:
        return 'Bem vindo Geek!'
    return 'Eu não tenho certeza de quem você é'


print(verifica_info())
print(verifica_info(1, 'Geek', True, 'University'))
print(verifica_info('University', 3.145))
"""


def soma_todos_numeros(*args):
    return sum(args)


numeros = [1, 2, 3, 4, 5, 6, 7]

num1, num2, num3, num4, num5, num6, num7 = numeros  # Desempacotamentos manual

# Desempacotamento automático passando como argumento a coleção antecedida do
# sinal de asterístico
print(soma_todos_numeros(*numeros))

