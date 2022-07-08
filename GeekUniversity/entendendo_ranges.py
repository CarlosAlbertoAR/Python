"""
Ranges

- Precisamos conhecer o loop for para usar os ranges.
- precisamos conhecer o range para trabalha melhor com loops for.

Ranges são utilizados para gerar sequencias numericas nao de forma aleatoria,
mas sim de maneire especificada.

Formas gerais:

Obs: Valor de parada não inclusive (início padrão 0, e passo de 1 em 1)
"""

# Forma 1 - Inicio padrão 0, passo padrão 1, o final apenas informado
# range(valor_de_parada)
for num in range(11):
    print(num)

# Forma 2 - Inicio especificado, passo padrão, final especificado
# range(valor_de_inicio, valor_de_parada)
for num in range(1, 11):
    print(num)

# Forma 3 - Inicio especificado, passo especificado, final especificado
# range(valor_de_inicio, valor_de_parada, passo)
for num in range(5, 50, 5):
    print(num)

# Forma 4 - Inversa( Inicio especificado, passo especificado, final especificado
# range(valor_de_inicio, valor_de_parada, passo)
for num in range(10, 0, -1):
    print(num)
