"""
Módulo Collections - Default Dict

https://docs.python.org/3/library/collections.html#collections.defaultdict
"""

# Recaptulando dicionarios
"""
dicionario = {'curso': 'Programacao em Python: Essencial'}

print(dicionario)

print(dicionario['curso'])

# print(dicionario['curso1']) # Chave não existente gera um KeyError
"""
# Default Dict - Ao criar uma dicionário utilizando-o, nós informamos um valor default,
# podendo informar uma lambda para isso. Este valor será utilizado sempre que não houver uma valor definido.
# Caso tentemos acessar uma chave que não existe, essa chave será criada e o valor default será atribuido.

# Fazendo import
# Obs: Lambdas são funções sem nome que podem ou não receber parametros de entrada e retornar valores

from collections import defaultdict

dicionario = defaultdict(lambda: 0)

print(dicionario)

dicionario['curso'] = 'Programação em Python: Essencial'

print(dicionario)

print(dicionario['outro']) # KeyError no dicionario comum, mas aqui não

print(dicionario)



