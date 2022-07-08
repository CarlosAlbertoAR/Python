"""
Reduce

OBS: A partir do Python 3+ a função reduce() não é mais uma função integrada (built-in). Portanto é necessário importar
o módulo 'functools'

Guido Van Rossum: Utilize a função reduce() se você realmente precisa dele. Em todo caso, 99% das vezes um loop é mais
legível.

Para entender o reduce()

Imagine que vocÊ tem uma coleção de dados:

dados = [a1, a2, a3, ..., an]

e você tem uma função que recebe dois parametros:

def funcao(x, y :
    :return x * y

Assim como map() e filter(), a função reduce() recebe dois parametros: a função e o iteravel

A função reduce(), funciona daseguinte forma:
    Passo 1: res1 = f(a1, a2)  # Aplica a função nos dois primeiros elementos da coleção e guarda o resultado
    Passo 2 : res2 = f(res1, a3)  # Aplica a função passando o resultado do passo 1 mais o terceiro elemento e guarda
    o res

    Isso é repetido até o final.
    Passo 3: res3 = f(res2, a4)
    .
    .
    .
    Passo n: resn = f(resm, an)

Ou seha, em cas passo ela aplica a função passando como primeiro argumento o resultado da execução anterior. No final
reduce() irá retornar o resultado final.

Alternativamente, poderíamos ver a função reduce() como:

funcao(funcao(funcao(a1, a2), a3), a4), ...), an)

"""

from functools import reduce

# Na prática, usando reduce() para multiplicar todos os números de uma lista

dados = [2, 3, 4, 5, 7, 11, 13, 17, 19, 23, 29]

# Criando a função de 2 parâmetros

multi = lambda x, y: x * y

res = reduce(multi, dados)
print(res)

# Utilizando um loop normal

res = 1
for n in dados:
    res = res * n

print(res)

