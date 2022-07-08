"""

Dicionários

Obs: Em algumas linguagens de programação, os dicionários Python são conhecidos por mapas.

Dicionários são coleções do tipo chave/valor.

Dicionários são representados por chaves {}.

Obs: sobre Dicionários
    - Chave e valor são seperados por dois pontos 'chave: valor'
    - Tanto chave quanto valor podem ser de qualquer tipo de dado
    - Podemos misturar tipo de dados;
    -
"""

# Criação de dicionários

# Forma 1 (Mais comum)
"""
paises = {'br': 'Brasil', 'eua': 'Estados Unidos', 'py': 'Paraguay'}

print(paises)
print(type(paises))
"""
# Forma 2 (Menos comun)
"""
paises = dict(br='Brasil', eua='Estados Unidos', py='Paraguay')

print(paises)
print(type(paises))
"""
# Acessando elementos

# Forma 1 - Acessando via Chave, da mesma forma que lista/tupla
# Ao tentar acessar uma palavra inexistente, ocorerá um erro de 'KeyError'
"""
print(paises['br'])
print(paises['py'])
"""
# Forma 2 - Acessando via get - Recomendada
# Ao tentar acessar uma palavra inexistente, ocorerá o retorno 'none' sem gerar um erro
"""
print(paises.get('br'))
print(paises.get('ru'))

russia = paises.get('ru')

if russia:
    print('Encontrado')
else:
    print('Não encontrado')
"""
# Get passando o valor padrão quando não encontrado
"""
pais = paises.get('py', 'Não encontrado')
print(f'encontrei o país {pais}')
"""

# Podemos verificar se determinda chave se encontra em um dicionário
"""
print('br' in paises)
print('ru' in paises)
print('Estados Unidos' in paises)

if 'ru' in paises:
    russia = paises['ru']
"""
# Podemos utilizar qualquer tipo de dados(int, float, string, boolean), inclusive lista, tupla dicionario, como chaves
# de dicionarios
"""
# Tupla como chave, são bastante interessantes de serem utilizadas como chave de dicionários
localidades = {
    (35.6895, 39.6917): 'Escritorio em Tókio',
    (40.7128, 74.0000): 'Escritorio em Nova York',
    (37.7749, 122.4194): 'Escritorio em São Paulo',
}

print(localidades)
print(type(localidades))
"""

# Adicionar elementos em um dicionário
"""
receita = {'jan': 100, 'fev': 120, 'mar': 300}

print(receita)
print(type(receita))

# Forma 1 - Mais comum

receita['abr'] = 350
print(receita)

# Forma 2

novo_dado = {'mai': 500}

receita.update(novo_dado)   # receita.update({'mai': 500})

print(receita)
"""
# Atualizando dados em um dicionario
"""
# Forma 1

receita.update({'jan': 150})

print(receita)

# Forma 2

receita.update({'mai': 600})

print(receita)

# CONSLUSÃO: A forma de adicionar novos elementos ou atualizar dados em um dicionário é a mesma
# CONSLUSÃO 2: Em dicionários, NÃO podemos ter chaves repetidas.
"""

# Remover dados de uma dicionário
"""
receita = {'jan': 100, 'fev': 120, 'mar': 300}
print(receita)

# Forma 1 - Mais comum

ret = receita.pop('mar')

print(receita)

# Obs: Aqui precisamos sempre informar a chave, e caso não encontre o elemento, um KeyError é retornado.
# Obs2: Ao removermos um objeto, o seu valor é sempre retornado ao chamar a função
"""
# Forma 2
"""
del receita['fev']

print(receita)

# Se a chave não existir será gravado um KeyError
# Obs: Neste caso o valor removido não é retornado.
"""

# Imagine que você sem um comércio eletrônico, onde temos um carrinho de compras no qual, adicionamos produtos.

"""
Carinho de compras:
    Produto 1:
        - nome;
        - quantidade;
        - preço;
    Produto 2:
        - nome;
        - quantidade;
        - preço;
        
"""
"""
# 1 - Poderíamos utilizar uma lista para isso? Sim

carrinho = []

produto1 = ['Playstation 4', 1, 2300.00]
produto2 = ['God of War', 1, 150.00]

carrinho.append(produto1)
carrinho.append(produto2)

print(carrinho)

# Teríamos que saber qual é o índice de cada informação no produto

# 2 - Poderíamos utilizar um tupla para isso? Sim

produto1 = ('Playstation 4', 1, 2300.00)
produto2 = ('God of War', 1, 150.00)

carrinho = (produto1, produto2)

print(carrinho)

# 3 - Poderíamos utilizar um dicionário para isto? Sim

carrinho = []

produto1 = {'nome': 'Playstation 4', 'quantidade': 1, 'preco': 2300.00}
produto2 = {'nome': 'God of War', 'quantidade' : 1, 'preco': 150.00}

carrinho.append(produto1)
carrinho.append(produto1)

print(carrinho)

# Desta forma, facilmente adicionamos ou removemos produtos do carrinho e em cada produto podemos ter a certeza
# sobre cada informação
"""

# Métodos de dicionários.

d = dict(a=1, b=2, c=3)

print(d)
print(type(d))

# Copiando um dicionário para outro

# Forma 1 - Deep Copy

novo = d.copy()
"""
print(novo)

novo['d'] = 4

print(d)
print(novo)
"""
# Forma 2 - Shallow Copy
"""
novo = d
print(novo)

novo['d'] = 4

print(d)
print(novo)
"""
# Forma não usual de criação de dicionários

outro = {}.fromkeys('a', 'b')

print(outro)
print(type(outro))

usuario = {}.fromkeys(['nome', 'pontos', 'email', 'profile'], 'desconhecido')

print(usuario)
print(type(usuario))

# O métido FromKeys recebe dois parâmetos: um iterável e um valor.
# Ele vai gerar para cada valor do iterável uma chave e irá atribuir a esta chave o valor informado.

veja = {}.fromkeys('teste', 'valor')

print(veja)

veja = {}.fromkeys(range(1, 11), 'novo')

print(veja)







