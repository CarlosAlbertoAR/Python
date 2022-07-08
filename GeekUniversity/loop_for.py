"""
Loop for

É uma estrutura de repetição

C ou Java

for(int i = 0; i < limitador; i++{
    //Execução do loop
}

Python

for item in interavel:
    //Execução do loop

Utilizamos loops para iterar sobre sequencias ou sobre valores iteráveis

Exemplos de iteráveis:
- String
    nome = 'Geek University'
- Lista
    lista = [1, 3, 5, 7, 9]
- Range
    numeros = range(1, 10)
"""
nome = 'Geek University'
lista = [1, 3, 5, 7, 9]
numeros = range(1, 10) # Tem que ser transformado em lista

# Exemplo de for 1 - Iterando em uma string
for letra in nome:
    print(letra)

# Exemplo de for 2 - Iterando sobre uma lista
for numero in lista:
    print(numero)

# Exemplo de for 2 - Iterando sobre um range
"""
range(valor_inicial, valor_final)
obs: o valor final não e inclusive;
1
2
3
4
5
6
7
8
9
10 - Não
"""
for numero in range(1, 10):
    print(numero)

"""
Enumerate:

((0, 'G'), (1, 'e'), (2, 'e'), (3, 'k'), (4, ' '), (5, 'U'))...

Obs : Quando não precisamos de uma valor, podemos descartá-lo utilizando um underline (_)     
"""

for indice, letra in enumerate(nome):
    print(nome[indice])

for indice, letra in enumerate(nome):
    print(letra)

# Desprezando o primeiro valor, sem utilizar variável
for _, letra in enumerate(nome):
    print(letra)

for valor in enumerate(nome):
    print(valor)

for valor in enumerate(nome):
    print(valor[0])

for valor in enumerate(nome):
    print(valor[1])

qtd = int(input('Quantas vezes esse loop deve executar? '))
for n in range(1, qtd+1):
    print(f'Imprimindo {n}')

soma = 0

for n in range(1, qtd+1):
    num = int(input(f'Informe o {n}/{qtd} valor: '))
    soma += num
print(f'A soma é {soma}')

# print com argumento de não separar o print com um salto de linha
nome = 'Geek University'
for letra in nome:
    print(letra, end='')

"""
Tabela de emogis unicode
https ://apps.timwhitlock.info/emogi/tables/unicode

Original: U+1F60D
Modificado: U0001F60D

"""

for num in range(1, 11):
    print('\U0001F60D' * num)




