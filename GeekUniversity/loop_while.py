"""
Loop while

Forma geral:

while expressao_booleana:
    //execução do loop

Expressão Booleana é toda expressão onde o resulta é verdadeiro ou falso.

Obs: Em um loo while, é importante que cuidemos do critério de parada, para não causar um loop infinito.

"""
numero = 1
while numero < 10:
    print(numero)
    numero += 1

# Exemplo 2
resposta = ''

while resposta != 'sim':
    resposta = input('Já acabou Jéssica? ')

