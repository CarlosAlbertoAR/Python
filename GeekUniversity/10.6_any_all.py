"""
Any e All

any() : Retorna True se pelo menos 1 dos valores é verdadeiro

all() : Retorna True se todos os elementos dos iterável são verdadeiros ou ainda se o iterável está vazio.

Obs um valor 0 (zero) para all será False

Um iterável vazio convertido para boolean é = False
o mesmo iterável convertido para all é = True, como dito acima
"""

# Exemplo all()

print(all([0, 1, 2, 3, 4]))  # Todos os números são verdadeiros? False por causa do 0 (zero)

print(all([1, 2, 3, 4]))  # Todos os números são verdadeiros? False por causa do 0 (zero)

print(all([]))  # Todos os números são verdadeiros? True

print(all(['Geek']))  # Todos os números são verdadeiros? True


# Usando all() com list comprehension
"""
nomes = ['Carlos', 'Camila', 'Carla', 'Cassioano', 'Cristina']

print(all([nome[0] == 'C' for nome in nomes]))  # True, todos começão com C

# Usando all() com for

nomes = (all([letra for letra in 'eio' if letra in 'aeiou']))  # True, pelo menos ema letra está na string iterável
print(nomes)


print(all([num for num in [4, 2, 10, 6, 8] if num % 2 == 0]))  # True

"""

# any()
"""
print(any([0, 1, 2, 3, 4]))  # True

print(any([0, False, {}, (), []]))  # False

nomes = ['Carlos', 'Camila', 'Carla', 'Cassioano', 'Cristina']  # True

print(any([nome[0] == 'C'for nome in nomes]))  # True

print(any([num for num in [4, 2, 10, 6, 8, 9] if num % 2 == 0]))  # FAlse

"""