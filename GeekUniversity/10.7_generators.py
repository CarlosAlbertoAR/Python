"""
Generator Expression

Em aulas anteriores nós estudamos:
- List Comprehension;
- Dictionary Comprehension;
- Set Comprehension

Não vimos:
- Tuple Comprehension... porque elas sem chamam Generators



print(any(nome[0] == 'C' for nome in nomes])
"""

from sys import getsizeof

# Podemos te feito utilizando Generators
"""
nomes = ['Carlos', 'Camila', 'Carla', 'Cassiano', 'Cristina', 'Vanessa']

print(any(nome[0] == 'C' for nome in nomes))
"""

# List Comprehension
"""
res = [nome[0] == 'C' for nome in nomes]
print(type(res))
print(res)
"""

# Generator - Mais performático
"""
res = (nome[0] == 'C' for nome in nomes)
print(type(res))
print(res)
"""

# Mostra quantos bytes a string 'Geek' ocupa em memória
"""
print(getsizeof('Geek'))
print(getsizeof(res))
"""

"""
# Gerando uma lista de números com List Comprehension
list_comp = getsizeof([x * 10 for x in range(1000)])

# Gerando uma lista de números com Set Comprehension
set_comp = getsizeof({x * 10 for x in range(1000)})

# Gerando uma lista de números com Dictionary Comprehension
dic_comp = getsizeof({x: x * 10 for x in range(1000)})

# Gerando um lista de números com Generator
gen = getsizeof(x * 10 for x in range(1000))

print('Para fazer a mesma tarefa gastamos em memória: ')
print(f'List Cmprehension: {list_comp} bytes')
print(f'Set Comprehension: {set_comp} bytes')
print(f'Dictionary Cmprehension: {dic_comp} bytes')
print(f'Generator Empression: {gen} bytes')
"""

# Iterando no Generator Expression
"""
gen = (x * 10 for x in range(1000))

for num in gen:
    print(num)
"""
