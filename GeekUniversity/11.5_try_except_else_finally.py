"""
try / except / else / finally

Dica de quando e onde tratar código:

TODA ENTRADA DEVE SER TRATADA!

- Bloco else -> É executado somento se não ocorrer o erro
- Bloco finally -> É sempre executado no término na função, independente se ouve excessão ou não
- O finally geralmente é utilizado para fechar ou desalocar recursos. (Conexão BD, Arquivo de escrita ou leitura, etc)

"""

# Exemplo prático

"""
try:
    num = int(input('Informe um número:'))
except ValueError:
    print('Valor incorreto')
else:
    print(f'Você digitou {num}')
finally:
    print('Programa finalizado')
"""

# Exemplo mais complexo

"""
def divide(a, b):
    return a / b

try:
    num1 = int(input('Informe o primeiro número: '))
except ValueError:
    print('O valor precisa ser numérico')

try:
    num2 = int(input('Informe o segundo número: '))
except ValueError:
    print('O valor precisa ser numérico')

try:
    print(divide(num1, num2))
except:
    print('Valor incorreto')
"""

# Exemplo mais complexo CORRETO, tratando na função as entradas individualmente
# OBS: Você é responsável pelas entradas das suas funções. Então trate-as!

"""
def dividir(a, b):
    try:
        return int(a) / int(b)
    except ValueError:
        return 'Valor incorreto'
    except ZeroDivisionError:
        return 'Não é possivel realizar um divisão por 0'


num1 = input('Informe o primeiro número: ')
num2 = input('Informe o segundo número: ')

print(dividir(num1, num2))
"""

# Exemplo mais complexo CORRETO, Genérico

"""
def dividir(a, b):
    try:
        return int(a) / int(b)
    except:
        return 'Ocorreu um problema'


num1 = input('Informe o primeiro número: ')
num2 = input('Informe o segundo número: ')

print(dividir(num1, num2))
"""

# Exemplo mais complexo CORRETO, semi-genérico
"""
def dividir(a, b):
    try:
        return int(a) / int(b)
    except (ValueError, ZeroDivisionError) as err:
        return f'Ocorreu um problema: {err}'


num1 = input('Informe o primeiro número: ')
num2 = input('Informe o segundo número: ')

print(dividir(num1, num2))
"""


