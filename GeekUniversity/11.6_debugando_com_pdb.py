"""
Debugando com PDB

PDB -> Python Debugger

Bug -> Inseto

"""

# A utilização do print() para debugar código é uma prática ruim

"""
def dividir(a, b):
    print(f'a = {a} b = {b}')
    try:
        return int(a) / int(b)
    except (ValueError, ZeroDivisionError) as err:
        return f'Ocorreu um problema: {err}'


print(dividir(4, 7))
"""


# Existem formas mais profissionais de se fazer esse 'debug', utilizando o debugger
# Em Python, podemos fazer isso em diferentes IDEs, com o o Pycharm ou o PDB - Python Debugger


# Exemplo cm o PyCharm
# Clicando ao lado da linha desejada, botão debug ou Shift + F8
# F8 para seguir ao proximo processamento


"""
def dividir(a, b):
    try:
        return int(a) / int(b)
    except (ValueError, ZeroDivisionError) as err:
        return f'Ocorreu um problema: {err}'


print(dividir(4, 0))
"""

# Exemplo com o PDB - Python Debugger - Exemplo 1
# Para utilizar o PDB, precisamos:
# Python < 3.6: Importar a biblioteca pdb e então utilizar a função set_trace()
# Python > 3.7: Não é mais necessário importar a biblioteca pdb, pois o comando debug foi incorporada como
# built-in, chamado agora de breakpoint()

# Comandos básicos do PDB
# l -> Listar onde estamos no código
# n -> Próxima linha
# p -> Imprime variável
# c -> Continua a exexução - Finaliza o debugging
"""
import pdb


nome = 'Angelina'
sobrenome = 'Jolie'
pdb.set_trace()
nome_completo = nome + ' ' + sobrenome
curso = 'Programação em Python Essencial'
final = nome_completo + ' faz o curso ' + curso
print(final)
"""

# Exemplo com o PDB - Python Debugger - Exemplo 2 fazendo o import no ponto do set_trace
# O debug é utilizado durante o desenvolvimento. Geralmente coloca-se os imports de blibiotecas no início do arquivo
# Portanto coloca-se o import pdb e set_trace() somente no ponto onde se quer debugar e depois pode ser removido

"""
nome = 'Angelina'
sobrenome = 'Jolie'
import pdb; pdb.set_trace()
nome_completo = nome + ' ' + sobrenome
curso = 'Programação em Python Essencial'
final = nome_completo + ' faz o curso ' + curso
print(final)
"""

# OBS: Cuidado com conflitos entre nomes de variáveis e os comando do pdb
# Neste caso como os nomes das variáveis são os mesmos dos comandos do pdb, para acessar avariável l por exemplo,
# devemos usar o comando "p" antes do nome da mesma. Ex: p nome_da_variavel

"""
def soma(l, n, p, c):
    breakpoint()
    return l + n + p + c


print(soma(1, 3, 5, 7))
"""

# Mas lembrese, nada de colocar nomes não representativos em variáveis. Sempre optar por nomes significativos.


