"""
Preservando metadata com wraps

Metadados -> São dados intrisecos em arquivos.

wraps -> São funções que envolvem elementos com diversas finalidades.

"""

# Problema


# Decorador

def ver_log(funcao):
    def logar(*args, **kwargs):
        """ Eu sou uma função (logar) dentro de outra"""
        print(f'Você está chamando: {funcao.__name__}')
        print(f'Aqui a documentação: {funcao.__doc__}')
        return funcao(*args, **kwargs)
    return logar


@ver_log
def soma(a, b):
    """ Soma dois números."""
    return a + b


print(soma(10, 20))  # Aqui OK

# Veja que o name e doc da função foi alterado pelo decorator, retornando as propriedades desse
print(soma.__name__)  # logar
print(soma.__doc__)  # Eu sou uma função (logar) dentro de outra

# Corrigindo de forma simples

from functools import wraps


def ver_log(funcao):
    @wraps(funcao)  # Preservando os metadados da função decoraqda
    def logar(*args, **kwargs):
        """ Eu sou uma função (logar) dentro de outra"""
        print(f'Você está chamando: {funcao.__name__}')
        print(f'Aqui a documentação: {funcao.__doc__}')
        return funcao(*args, **kwargs)
    return logar


@ver_log
def soma(a, b):
    """ Soma dois números."""
    return a + b

print(soma(10, 20))  # Aqui OK

# Veja que o name e doc da função foi alterado pelo decorator, retornando as propriedades desse
print(soma.__name__)  # logar
print(soma.__doc__)  # Eu sou uma função (logar) dentro de outra
