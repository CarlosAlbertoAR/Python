"""
O Bloco try/except

Utilizamos o bloco tr/except para traar erros que podem ocorrer no nosso código. Previnindo assim que o programa pare de
 e o usuáro receba mensagens de erro inesperadas.

try:
    //execução problemática
except:
    //o que deve ser feito em caso de problema

"""

# Exemplo 1 - Tratando um erro genérico
# Tente executar a função geek(), caso encontre algum erro, imprima a mensagem de erro
"""
try:
    geek()
except:
    print('Opa, algum problema com a função')
"""

# Exemplo 2 - Tratando um erro genérico
# Tente executar a função len() passando como argumento 5, caso encontre algum erro, imprima a mensagem de erro
"""
try:
    len('5')
except:
    print('Opa, algum problema com a função')
"""

# OBS: Tratar de forma genérica ão é a melhor forma de tratamento de erros. o ideal é SEMPRE tratar de forma específica.

# Exemplo 3 - Tratando um erro específico NameError
"""

try:
    geek()
except NameError:
    print('Você está tetando utilizar uma função enexistente')
"""

# Exemplo 4 - Tratando um erro específico TypeError

"""
try:
    len(5)
except TypeError:
    print('Você passando um argumento inapropriado')
"""

# Exemplo 5 - Tratando um erro específico e capturando detalhes do erro

"""
try:
    len(5)
except TypeError as err:
    print(f'A aplicação gerou o seguinte erro: {err}')  # object of type 'int' has no len()
"""

# Podemos efetuar diversos tratamentos de erros de uma vez.
"""
# a)

try:
    print('geek'[9])
except NameError as erra:
    print(f'Deu NameError: {erra}')
except TypeError as errb:
    print(f'Deu TypeError: {errb}')
except:
    print('Deu um erro diferente')

# b)

def pega_valor(dicionario, chave):
    try:
        return dicionario[chave]
    except KeyError:
        return None
    except TypeError:
        return None


dic = {"nome": "Geek"}

print(pega_valor(dic, 'game'))  # Tratamento de KEyError, None

print(pega_valor(7, 'game'))  # Tratamento de TypeError, None
"""




