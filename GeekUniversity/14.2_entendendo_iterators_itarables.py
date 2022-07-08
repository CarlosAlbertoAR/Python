"""
Entendendo Iterators e Iterables

Iterator ->
    - Um objeto que pode ser iterado.
    - Um objeto que retorna um dados, sendo um elemento por ver quando uma função next() é chamdada;

Iterable ->
    - Um objeto que irá retornar um iterator quando a função iter() for chamada.

"""

nome = 'Geek'  # É um iterable mas não é um iterator.
numeros = [1, 2, 3, 4, 5, 6]  # É um iterable mas não é um iterator.

"""
# Transformando interables em interators

it1 = iter(nome)
it2 = iter(numeros)

print(next(it1))  # G
print(next(it1))  # e
print(next(it1))  # e
print(next(it1))  # k

# print(next(it1))  # StopIterator Error

print(next(it2))  # 1
"""

# Quando executado o for abaixo Python transforma nome em um iterator com iter() e o roda comando next() até o fim,
# sem que ultrapasse o final

for letra in nome:
    print(letra)



