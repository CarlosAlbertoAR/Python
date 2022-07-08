"""
Módulo Random e que são múdulos

- Em Python, múdulos nada mais são que outros arquivos Python.
- São úteis para que possamos deixas nossos programas mais simples e para que possamos reutilizar código

Módulo Random -> Possui várias funções para geração de números pseudo-aleatórios
"""

# OBS: Existem 2 formas de se utilizar um módulo ou função deste

# Forma 1 - Importando todo o módulo (Não recomendado)

import random

# Ao realizar o import de todo o módulo, todas as funções, atributos, classes e propriedades que estiverem dentro do
# módulo ficarão disponíveis (Ficando em memória). Caso você saiba quais funções você precisa utilizar do múdolo, então
# esta não seria a forma ideal de utilização. Nós veremos uma forma melhor na forma 2.
"""
print(random.random())
"""

# Veja que apara utilizar a função ramdom() do pacote ramdom, colocamos o nome do pacote e nome da função separados por
# ponto

# OBS: Não confunda a função ramdom() com o pacote random. Pode parecer confuso, mas a função random() é uma função
# dentro do módulo homonimo


# Forma 2 - Importando uma função específica do múdilo (Forma recomendada)
# random() -> Gerar um número real pseudo-aleatório entre os valores 0 e 1
"""
from random import random

# No import acima, estamo falando: Do múdulo random, importe a função random

for i in range(10):
    print(random())
"""

# uniform() -> Gera um número real pseudo-aleatório entre os valores estabelecidos
"""
from random import uniform

for i in range(10):
    print(uniform(3, 7))  # 7 não está incluso
"""

# randint() -> Gera um valor pseudo-aleatório entre os valores estabalecidos.
"""
from random import randint

# Gerador de apostas para mega-sena
for i in range(6):
    print(randint(1, 61), end=', ')  # Começa em 1 e vai até 60
"""

# choice() -> Mostra um valor aleatório entre um iterável
"""
from random import choice

jogadas = ['pedra', 'papel', 'tesoura']

print(choice(jogadas))
"""

# shuffle() -> Tem a função de embaralhar dados
"""
from random import shuffle

cartas = ['K', 'Q', 'A', '2', '3', '4', '5', '6', '7']

shuffle(cartas)
print(cartas)

shuffle(cartas)
print(cartas)
"""


