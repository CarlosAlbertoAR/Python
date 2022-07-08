"""

Listas (list)

Listas em Python funcionam como vetores/matrizes (arrays) em outras linguagens, com a diferença
de serem DINâMICO e também de podermos colocar QUALQUER tipo de dado.

Linguagens C/Java: Arrays
    - Possuem tamanho e tipo dado fixo;
    Ou seja, nestas linguagens se vc criar uma array do tipo int e com tamanho 5, este array
    será SEMPRE do tipo inteiro e poderá ter SEMPRE no máximo 5 valores.

Já em Python
    - Dinâmico: Não possui tamanho fixo; Ou seja, podemos criar a lista e simplesmente ir adicionando elementos;
    - Qualquer tipo de dado: Não possuem tipo de dado fixo; Ou seja, podemos colocar qualquer tipo de dado;

As listas em Python são representadas por colchetes: []

São mutáveis, podem mudar constantemente
"""

type([])

lista1 = [1, 99, 4, 27, 15, 22, 3, 1, 44, 42, 27]

lista2 = ['G', 'e', 'e', 'k', ' ', 'U', 'n', 'i', 'v', 'e', 'r', 's', 'i', 't', 'y']

lista3 = []

lista4 = list(range(11))

lista5 = list('Geek University')

# Podemos facilmente checar se determinado valor está contido na lista
"""
if 8 in lista4:
    print('Encontrei o número 8')
else:
    print('Não encontrei o número 8')
"""
# Podemos facilmente ordenar uma lista
"""
lista1.sort()
print(lista1)
"""
# Podemos facilmente contar o número de ocorrencia de uma valor em uma lista
"""
print(lista1.count(1))
print(lista5.count('e'))
"""
# Adicionar elementos em listas

"""
Para adicionar elementos em listas, utilizamos a função append()

Obs:  Com append, nós só consegimos adicionar 1 elemento por vez
list1.append(12, 34, 56)
"""
"""
print(lista1)
lista1.append(42)
print(lista1)
"""
# Qualquer tipo de dado dentro da lista, inclusive outra lista
"""
lista1.append([8, 3, 1])
print(lista1)

if [8, 3, 1] in lista1:
    print('Encontrei na lista')
else:
    print('Não encontrei na lista')
"""
# Adicionando mais elementos de uma única vez
"""
lista1.extend([123, 44 ,67])
print(lista1)
"""
# Podemos inserir um novo elemento na lista informando a posição do índice
# O que não substitui o valor que lá estava, o mesmo é deslocado para direita
"""
lista1.insert(2, 'novo valor')
print(lista1)
"""
# Podemos facilmente juntar duas listas
"""
lista6 = lista1 + lista2
print(lista6)
"""
# Podemos facilmente inverter uma lista

# Forma 1
# lista1.reverse()
# lista2.reverse()
"""
print(lista1)
print(lista2)

print(lista1[::-1])
print(lista2[::-1])
"""
# Copiar uma lista
"""
lista6 = lista2.copy()
print(lista6)
"""
# Tamanho de uma lista
"""
print(len(lista1))
"""
# Podemos remover facilmente o ultimo elemento de uma lista
# Obs : Não somente remove o ultimo elemento como também o retorna
"""
print(lista5)/
lista5.pop()
print(lista5)
"""

# Passando o indice, ele é removido, o default é o ultimo
# Obs: Os elementos a direita deste indice serão deslocados par a esquerda.
# Obs : Se não houver elemento no índice informado, reremos o erro IndexError
"""
print(lista5)
print('removido: ' + lista5.pop(0))
print(lista5)
"""
# Podemos facilmente remover todos os elementos (zerar a lista)
"""
print(lista5)
lista5.clear()
print(lista5)
"""

# Podemos facilemente repetir elementos em uma lista
"""
nova = [1, 2, 3]
print(nova)
nova *= 3
print(nova)
"""
# Podemos facilmente converter uma string para uma lista
# Exemplo 1

# Obs: Por padrão, o split separa os elementos da lista pela espaço entre elas
"""
curso = 'Programação em Python: Essencial'
print(curso)
curso = curso.split()
print(curso)
"""
# Exemplo 2

# Obs: Passando o separador
"""
curso = 'Programação,em,Python:,Essencial'
print(curso)
curso = curso.split(',')
print(curso)
"""
# Convertendo uma lista eme uma string
"""
lista6 = ['Programação', 'em', 'Python:', 'Essencial']
print(lista6)
"""
# Abaixo, para cada elemento da lista6, adiciona espaço e transforma em única string
"""
curso = ' '.join(lista6)
print(curso)
"""
# Por cifrão ou outro caractere qualquer ao invés de espaço
"""
curso = '$'.join(lista6)
print(curso)
"""
# Podemos realmente colocar qualquer tipo de dado em uma lista, inclusive mistutrando esses dados
"""
lista9 =[1, 2.34, True, 'Geek', 'd', [1, 2, 3], 4534453445345]
print(lista6)
print(type(lista6))
"""
# Iterando sobre lista
# Podendo ser tanto entre numeros ou entre strings (lista 1 e lista 2)

# Exemplo 1 - Utilizando for
"""
soma = ''
for elemento in lista2:
    print(elemento)
    soma = soma + elemento
print(lista2)
print(f'Soma: {soma}')
"""
# Exemplo 2 - Utilizando while
"""
carrinho = []
produto = ''

while produto != 'sair':
    print("Adicione um produto na lista ou digite 'sair' para sair")
    produto = input()
    if produto != 'sair':
        carrinho.append(produto)

for produto in carrinho:
    print(produto)

print(f'Carrinho = {carrinho}')
"""

# Utilizando variaveis em listas
"""
numeros = [1, 2, 3, 4, 5]

num1 = 1
num2 = 2
num3 = 3
num4 = 4
num5 = 5

numeros = [num1, num2, num3, num4, num5]
print(numeros)
"""
# Fazemos acesso aos elementos de forma indexada
#           0         1        2        3
"""
cores = ['verde', 'amarelo', 'azul', 'branco']

print(cores[0])  # verde
print(cores[1])  # amarelo
print(cores[2])  # azul
print(cores[3])  # branco
"""
# Podemos fazer o acesso de forma indexada inversa
# Pense na lista como se fosse um circulo
"""
print(cores[-1])  # branco
print(cores[-2])  # azul
print(cores[-3])  # amarelo
print(cores[-4])  # verde
# print(cores[-5])  # Erro, pois não existe
"""

# Loops
"""
cores = ['verde', 'amarelo', 'azul', 'branco']

for cor in cores:
    print(cor)

indice = 0
while indice < len(cores):
    print(cores[indice])
    indice += 1
"""
# Gerar indice em um for
"""
cores = ['verde', 'amarelo', 'azul', 'branco']
for indice, cor in enumerate(cores):
    print(indice, cor)

corespar = list(enumerate(cores))
print(corespar)
"""

# Listas permitem valores repetidos
"""
lista = []
lista.append(42)
lista.append(42)
lista.append(42)
lista.append(33)
lista.append(42)

print(lista)
"""
# Outros métodos não tão importantes mas também úteis

# Encontrar o índice de ume elemento na lista

comida = ['arroz', 'feijão', 'macarrão', 'bife', 'feijão']
"""
print(comida.index('bife'))
"""

# Obs: Caso não haja o elemento procurado na lista, será apresentado erro ValueError
"""
print(comida.index('salada'))
"""

# Obs: Em caso de itens repetidos, retorna o indice do primeiro encontrado
"""
print(comida.index('feijão'))
"""
# Podemos fazer busca dentro de um range, ou seja, a partir de qual indice começar a buscar
# Obs: Caso não haja o elemento procurado na lista, será apresentado erro ValueError
"""
print(comida.index('feijão', 3))  # buscando 'feijão' a partir do índice 3
"""
# Podemos fazer busca dentro de um range, inicio/fim
"""
print(comida.index('feijão', 2, 5))  # Passado um indice a mais, senão não encontra
print(comida.index('arroz', 0, 5))
"""
# Revisão de slicing

# lista[inicio:fim:passo]
# range(inicio:fim:passo)

lista = [1, 2, 3, 4]

# Trabalhando com slice de lista com o parâmetro 'inicio'
"""
print(lista[::])  # Listando todos os elementos
print(lista[1:])  # Iniciando no índice 1 e pegando todos os elementos restantes
print(lista[1:])  # Iniciando no índice 1 e pegando todos os elementos restantes
"""
# Trabalhando com slice de lista com o parâmetro 'fim'
"""
print(lista[:2])  # Iniciando no índice 0 e pegando até o índice 2 - 1
print(lista[:4])  # Iniciando no índice 0 e pegando até o índice 4 - 1
print(lista[1:3])  # Iniciando no índice 1 e pegando até o índice 3 - 1
"""
# Trabalhando com slice de lista com o parâmetro 'passo'
"""
print(lista[1::2])  # Iniciando no índice 1 e pegando até o final, de 2 em 2
print(lista[::2])  # Iniciando no índice 0 e pegando até o o final, 2 em 2
print(lista[1::-1])  # Iniciando no índice 1 e pegando até o final, de trás pra frente
"""

#  Invertendo valores em uma lista
"""
nomes = ['Geek', 'University']

nomes[0], nomes[1] = nomes[1], nomes[0]
print(nomes)

nomes.reverse()
print(nomes)
"""

# Soma*, Valor Máximo*, Valor Mínimo*, Tamanho
# Se os valores da lista forem inteiros o reais.
"""
lista = [1, 2, 3, 4, 5, 6]
print(sum(lista))  # soma
print(min(lista))  # mínimo valor
print(max(lista))  # máximo valor
print(len(lista))  # tamanho da lista
"""
# Transformar uma lista em tupla
"""
lista = [1, 2, 3, 4, 5, 6]
print(lista)
print(type(lista))

tupla = tuple(lista)
print(tupla)
print(type(tupla))
"""
# Desempacotamento de listas
# Obs: O números de variaveis e elementos devem ser iguais, caso contrário surge um ValueError
"""
lista = [1, 2, 3]

num1, num2, num3 = lista

print(num1)
print(num2)
print(num3)
"""

# Copiando uma lista para outra (Shallow Copy e Deep Copy)

# Forma 1 - Deep copy
# .copy tornam se totalmente independentes, modificando uma, não afeta outra
"""
original = [1, 2, 3]
print(original)

nova = original.copy()
print(nova)
nova.append(4)
print(nova)
print(original)
"""
# Forma 2 - Shallow Copy
# Cópia via atribuição, após realizar modificação em uma das listas, essa modificação se refletiu em ambas
"""
original = [1, 2, 3]
print(original)

nova = original
print(nova)
nova.append(4)
print(nova)
print(original)
"""






