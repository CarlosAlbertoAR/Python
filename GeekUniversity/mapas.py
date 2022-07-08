"""
Mapas -> Conhecidos em Python como Dicionários

Dicionários em Python são representados por chaves {}
"""

receita = {'jan': 100, 'fev': 250, 'mar': 400}

# Iterar sobre dicionários
"""
for chave in receita:
    print(chave)

for chave in receita:
    print(receita[chave])
    
for chave in receita.keys(): # Modo Pythonico
    print(receita[chave])

for chave in receita:
    print(f'{chave} : {receita[chave]}')
"""

# Acessando as chaves do dicionário
"""
print(receita.keys())
"""
# Acessando os valores
"""
print(receita.values())

for valor in receita.values():
    print(valor)
"""
# Desempacotamento de dicionários
"""
print(receita.items())  # Dicionário de tuplas chave/valor

for chave, valor in receita.items():
    print(f'chave={chave} e valor={valor}')
"""
# Soma*, Valor Máximo*, Valor Mínimo*, Tamanho

# * Se os valores forem todos inteiros ou reais
"""
print(sum(receita.values()))
print(max(receita.values()))
print(min(receita.values()))
print(len(receita))
"""
