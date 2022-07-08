"""
Erros mais comuns em Python

ATENÇÂO:

- É impostante prestar atenção e aprender a ler as saídas de erros geradas pela execução do nosso código.

- Exception e Erros são sinônimos na programação.
"""

# 1 - SyntaxError -> Ocorre quando o Pythin encontra um erro de sintaxe. Ou seja, você escreveu algo que o Pythin não
# reocnhece como parte da Linguagem.

# a)
"""
def funcao:  # Falta de parentese ao definir função "SyntaxError: invalid syntax", correto def funcao():...
    print('Geek University')
"""

# b)
"""
def = 1  # Utilzando uma palavra reservada da liguagem como variável  "SyntaxError: invalid syntax"
"""

# 2 - NameError -> Ocorre quando uma variável ou função não foi definida.

# a)
"""
print(geek)  # NameError: name 'geek' is not defined
"""

# b)
"""
geek()  # NameError: name 'geek' is not defined
"""

# c)
"""
a = 18
# Alternativa ao erro seria inicializar a variável antes do bloco if
# msg = 'É maior que 10'

if a < 10:
    msg = 'É menor que 10'

print(msg)  # msg não será definida quando a for maior que 10  "NameError: name 'msg' is not defined"
"""

# 3 - TypeError - Ocorre quando uma função/operação/ação é aplicada a um tipo errado

# a)
"""
print(len(5))  # len() só se aplica a iteráveis "TypeError: object of type 'int' has no len()"
"""

# b)
"""
print('Geek' + [])  # Erro ao concatenar string e lista "TypeError: can only concatenate str (not "list") to str"
"""

# 4 - IndexError -> Ocorre quando tentamos acessar uma elemento em uma lista ou outro tipo de dados indexado utilizando
# um índice inválido.

# a)
"""
lista = ['Geek']
print(lista[2])  # Tentando acessar item indice 2 numa lista "IndexError: list index out of range"
"""

# b)
"""
lista = ['Geek']
print(lista[0][10])  # Tentando acessar a posição 10 da primeira lista "IndexError: string index out of range"
"""

# c)
"""
tupla = ('Geek')
print(tupla[0][10]) # Tentando acessar a posição 10 da primeira tupla "IndexError: string index out of range"
"""

# 5 - ValueError -> Ocorre quando uma função/operação built-in (integrada) recebe um argumento com o tipo correto, mas
# valor inapropriado

# a)
"""
print(int('Geek'))  # Conventendo letra para int "ValueError: invalid literal for int() with base 10: 'Geek'"
"""

# 6 - KeyError -> Ocorre quando tentamos acessar um dicionário com uma chave que não existe

# a)
"""
dic = {'nome': 'Carlos'}
print(dic['geek'])  # Tentando acessar uma chave não existente "KeyError: 'geek'"
"""

# 7 - AttributeError -> Ocorre quando uma variável não tem um atributo/função

# a)
"""
tupla = (11, 2, 31, 4)
print(tupla.sort())  # Tentanto usar o métido sort na tupla "AttributeError: 'tuple' object has no attribute 'sort'"
"""

# 8 - IdentationError -> Ocorre quando não respeitamos a identaçao do Python (4 espaços)

# a)
"""
def nova():
print('Geek')  # Não efetuada a identação de um bloco esperada "IndentationError: expected an indented block"
"""

# b)
"""
for i in range(10)
i + 1  # Não efetuada a identação de um bloco esperada "IndentationError: expected an indented block"    
"""


