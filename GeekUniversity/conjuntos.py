"""
Conjuntos

- Conjuntos em linguagem de programação, estamos fazendo referencia a teoria dos Conjuntos da Matemática.

- Aqui no Python os conjuntos são chamados de Sets.

Dito isto, da mesma forma que na matemática:

- Sets (conjntos) não possuem valores duplicados;
- Sets (conjntos) não possuem valores ordenados;
- Elementos não são acessado via índice, ou seja conjunto não são indexados;

Conjuntos são bons para se utilizar quando precisamos armazenar elementos mas não nos importamos com a ordenação deles.
Quando não precisamos se preocupar com chaves, valores e itens duplicados.

Os conjuntos (sets) são referenciados em Python com chaves {}

Diferença entre Conjuntos (Set) e Mapas (Dicionários) em Python:
    - Um dicionário tem chave/valor;
    - Um conjunto tem apenas valor;
"""

# Definindo um conjunto:

# Forma 1
"""
s = set({1, 2, 3, 4, 5, 5, 6, 7, 2, 3}) # Repare que temos valores repetidos

print(s)
print(type(s))
"""
# Obs: Ao criar um conjunto, caso seja adicionado um valor já exitente, o mesmo será ignorado sem gerar erro e não
# fará parte do conjunto.

# Forma 2 - Mais comum
"""
s = {1, 2, 3, 4, 5, 5, 6, 7, 2, 3}
print(s)
print(type(s))

# Podemos verificar se determinado elemento está contido no conjunto

if 3 in s:
    print('Tem o 3')
else:
    print('Não tem o 3')
"""

# Importante lembrar que, além de não termos valores duplicados, não temos ordem
"""
# Listas aceitam valores duplicados, então temos 10 elementos
lista = [99, 2, 34, 23, 2, 12, 1, 44, 5, 34]
print(f'Lista: {lista} com {len(lista)} elementos')

# Tuplas aceitam valores duplicados, então temos 10 elementos
tupla = (99, 2, 34, 23, 2, 12, 1, 44, 5, 34)
print(f'Tupla: {tupla} com {len(tupla)} elementos')

# Dicionários não aceitam chaves duplicados, então temos 8 elementos
dicionario = {}.fromkeys([99, 2, 34, 23, 2, 12, 1, 44, 5, 34], 'dict')
print(f'Dicionário: {dicionario} com {len(dicionario)} elementos')

# Conjuntos não aceitam valores duplicados, então temos 8 elementos
conjunto = {99, 2, 34, 23, 2, 12, 1, 44, 5, 34}
print(f'Conjunto: {conjunto} com {len(conjunto)} elementos')
"""
# Assim como outro conjunto Python, podemos colocar todos os tipoas de dados misturados em Sets
"""
s = {1, 'b', True, 34.22, 44}

print(s)
print(type(s))
"""
# Podemos iterar em um set normalmente
"""
for valor in s:
    print(valor)
"""

# Usos interessantes em sets

# Imagine que fizemos um formulário de cadastro de visitantes em uma feira ou museu e os visitantes
# informam manualmente a cidade de onde vieram.

# Nós adicionamos cada cidade em uma lista Python, já que em uma lista podemos adicionar novos elementos
# e ter repetição.
"""
cidades = ['Belo Horizonte', 'São Paulo', 'Campos Grande', 'Cuiaba', 'Campo Grande', 'São Paulo', 'Cuiaba']

print(cidades)
print(len(cidades))

# Agora precisamos saber quantas cidades distintas/únicas tempos.

# O que você faria? Faria um loop na lista?

# Podemos utilizar o set para isto:

print(len(set(cidades)))
"""

# Adicionando elementos em um conjunto
"""
s = {1, 2, 3}
print(s)

s.add(4)
s.add(4)  # Duplicidade não gera erro
print(s)
"""
# removendo elementos em um conjunto
# Obs: Se o valor não foi encontrado, será gerado o erro KeyError

# Forma 1 - Nenhum valor é retornado
"""
s.remove(3)  # Não é indice, informamos o valor a ser removido

print(s)
"""
# Forma 2
"""
s.discard(2)

print(s)
"""
# Copiando um conjunto para outro
"""
s = {1, 2, 3}

# Forma 1 - Deep Copy

novo = s.copy()
print(novo)

novo.add(4)

print(novo)
print(s)
"""
# Forma 2 - Shallow Copy
"""
novo = s
print(novo)

novo.add(4)

print(novo)
print(s)
"""
# Podemos remover todos os itens de um conjunto
"""
s = {1, 2, 3}
s.clear()
print(s)
"""
# Métodos Matemáticos de conjuntos
"""
# Imagine que temos 2 conjuntos: Um contendo estudando do curso Python e um estudante do curso de Java

estudantes_python = {'Marcos', 'Patricia', 'Ellen', 'Pedro', 'Julia', 'Guilherme'}
estudantes_java = {'Fernando', 'Gustavo', 'Julia', 'Ana', 'Patricia'}

# Veja que alguns alunos que estudam Python também estudam Java.

# Precisamos gerar um conjuntos com nomes de estudante únicos

# Forma 1 - Utilizando uniom - Recomendado

unicos1 = estudantes_java.union(estudantes_python)
# {'Julia', 'Gustavo', 'Ellen', 'Marcos', 'Pedro', 'Ana', 'Patricia', 'Fernando', 'Guilherme'}
print(unicos1)

unicos1 = estudantes_python.union(estudantes_java)
# {'Patricia', 'Marcos', 'Fernando', 'Guilherme', 'Julia', 'Pedro', 'Gustavo', 'Ellen', 'Ana'}
print(unicos1)

# Forma 2 - Utilizando o caracter Pipe |

unicos2 = estudantes_python | estudantes_java

print(unicos2)

"""
# Precisamos gerar um conjunto de estudanres que estão em ambos os cursos
"""
# Forma 1 - Utilizando intersection

ambos1 = estudantes_java.intersection(estudantes_python)

print(ambos1)

# Forma 2 - Utilizando & comercial

ambos2 = estudantes_java & estudantes_python

print(ambos2)
"""
# Gerar um conjunto de estudantes que não estão no outro curso
"""
so_python = estudantes_python.difference(estudantes_java)
print(so_python)

so_Java = estudantes_java.difference(estudantes_python)
print(so_Java)
"""
# Soma*, Valor Máximo*, Valor Mínimo*, Tamanho

# * Se os valores forem todos inteiros ou reais

s = {1, 2, 3, 4, 5, 6}

print(sum(s))
print(max(s))
print(min(s))
print(len(s))






