"""
Levantando os próprios erros com raise

raise -> Lança exceções

OBSERVAÇÔES:

1 - O raise não é uma função. É uma palavra reservada, assim como def, ou qualque outra em Python

2 - O raise assim como como o return, finaliza a função. Ou seja, nada após a raise é executado.

Para simplificar, pense mo raise como sendo útil para que possamos criar nossas próprias exceções e mensagens de erro.

A forma geral de utilização é:

raise tipoDoErro('Mensagem de erro')
"""

# Exemplo

"""
def colore(texto, cor):
    if type(texto) is not str:
        raise TypeError('Texto precisa ser uma string')
    if type(cor) is not str:
        raise TypeError('Cor precisa ser uma string')
    print(f'O texto {texto} será impresso na cor {cor}')


colore('Geek', 2)  # TypeError: Cor precisa ser uma string

colore(10, 'azul')  # TypeError: Texto precisa ser uma string

colore('Geek', 'azul')  # ok
"""

# Exemplo refatorado

"""
def colore(texto, cor):
    cores = ('verde', 'amarelo', 'azul', 'branco')
    if type(texto) is not str:
        raise TypeError('Texto precisa ser uma string')
    if type(cor) is not str:
        raise TypeError('Cor precisa ser uma string')
    if cor not in cores:
        raise ValueError(f'A cor precisa ser uma entre {cores}')
    print(f'O texto {texto} será impresso na cor {cor}')


colore('Geek', 'lilas')  # ValueError: A cor precisa ser uma entre ('verde', 'amarelo', 'azul', 'branco')
"""



