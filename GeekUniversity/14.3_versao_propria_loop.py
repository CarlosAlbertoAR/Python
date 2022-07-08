"""
Criando sua própria versão de loop

"""

"""
# For comum

for num in [1, 2, 3, 4, 5]:
    print(num)

for letra in 'Geek University':
    print(letra)
"""

# Versão própria de for


def meu_for(iteravel):
    it = iter(iteravel)
    while True:
        try:
            print(next(it))
        except StopIteration:
            break

# Testando

meu_for('Geek University')


