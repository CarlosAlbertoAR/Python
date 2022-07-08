"""
Módulo Collections - Deque

https://docs.python.org/3/library/collections.html#collections.deque

Podemos dizer que o deque é uma lista de alta performance.
"""

# import
from collections import deque

# Criando deques

deq = deque('geek')

print(deq)

# Adiconando elementos no deque

deq.append('y')  # Adiciona no final

print(deq)

"""
Diferença do deque para lista
"""

# Adicionando no começo
deq.appendleft('k')  # Adiciona no começo

print(deq)

# Removendo elementos

print(deq.pop())  # Remove e retorna o último elemento

print(deq)

print(deq.popleft())  # Remove e retorna o primeiro elemento

print(deq)
