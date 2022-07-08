"""
**kwargs

Poderíamos chamar este parâmetro de **xis mas por convenção chamamos de **kwargs

Este é só mais um parâmetro, mas diferente do *args que coloca os valores extras em uma tupla, p **kwargs exique que
utilizemos parâmetros nomeados, e transforma esses parâmetros extras em um dicionário.
"""

# Exemplo
"""

def cores_favoritas(**kwargs):
    for pessoa, cor in kwargs.items():
        print(f'A cor favorita de {pessoa.title()} é {cor}')

cores_favoritas(marcos='verde', julia='amarelo', fernanda='azul', vanessa='branco')


# OBS : Os parÂmetros *args e **kwargs não são obrigatórios.

cores_favoritas()

cores_favoritas(marcos='verde')
"""

# Exemplo mais complexo
"""

def cumprimento_especial(**kwargs):
    if 'geek' in kwargs and kwargs['geek'] == 'Python':
        return 'Você recebeu um cumprimento Pythônico Geek'
    elif 'geek' in kwargs:
        return f"{kwargs['geek']} Geek!"


print(cumprimento_especial())
print(cumprimento_especial(geek='Python'))
print(cumprimento_especial(geek='Oi'))
print(cumprimento_especial(geek='especial'))
"""

# Nas nossas funções podemos ter (NESTA ORDEM):
"""
# Parâmetros obrigatórios
# *args
# Parâmetros default (não obrigatórios)
# **kwargs


def minha_funcao(idade, nome, *args, solteiro=False, **kwargs):
    print(f'{nome} tem {idade} anos')
    print(args)
    if solteiro:
        print('Solteiro')
    else:
        print('Casado')
    print(kwargs)


minha_funcao(8, 'Julia')
minha_funcao(18, 'Felicity', 4, 5, 3, solteiro=True)
minha_funcao(34, 'Felipe', eu='Não', voce='Vai')
minha_funcao(19, 'Carla', 9, 4, 3, java=False, python=True)
"""
# Entenda porque é importante manter a ordem dos parâmetros na declaração
"""

# Função com a ordem correta de parâmetros
def mostra_info(a, b, *args, instrutor='Geek', **kwargs):
    return [a, b, args, instrutor, kwargs]
"""
"""
Resultado
a = 1
b = 3
args = (3)
instrutor = 'Geek'
kwargs = {'sobrenome': 'University', 'cargo': 'Instrutor'}
"""

# Função com a ordem incorreta de parâmetros
"""

def mostra_info(a, b, instrutor='Geek', *args,  **kwargs):
    return [a, b, args, instrutor, kwargs]

# Resultado [1, 2, (), 3, {'sobrenome': 'University', 'cargo': 'Instrutor'}]

print(mostra_info(1, 2, 3, sobrenome='University', cargo='Instrutor'))
"""

# Desempacotar com **kwargs
"""
def mostra_nomes(**kwargs):
    return f"{kwargs['nome']} {kwargs['sobrenome']}"

nomes = {'nome': 'Felicity', 'sobrenome': 'Jones'}

print(mostra_nomes(nomes))  # TypeError
print(mostra_nomes(**nomes))  # Desempacotando
"""

# Desempatotando kwargs em função que não contém parametro kwargs
"""

def soma_multiplos_numeros(a, b, c):
    print(a + b + c)


soma_multiplos_numeros(1, 2, 3)

lista = [1, 2, 3]
tupla = (1, 2, 3)
conjunto = {1, 2, 3}
soma_multiplos_numeros(*lista)

dicionario = dict(a=1, b=2, c=3)
soma_multiplos_numeros(**dicionario)

# OBS: Os nomes da chave em um dicionário devem se os mesmos dos parâmetros da função

dicionario = dict(d=1, b=2, c=3)
soma_multiplos_numeros(**dicionario) # TypeError
"""

