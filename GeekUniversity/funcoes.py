"""

Definindo funções

- Funções são pequenos partes de código que realizam tarefas especificas;
- Pode ou não receber entrada de dados e retornar uma saída de dados;
- Muito uteis para executar procedimento similares por repetidas vezes;

- DRY - Don´t Repeat Youself - Não repita seu código

Obs: Se você escrever uma função que realiza várias tarefas dentro dela,
é bom fazer uma verificação para que a função seja simplificada.

Já utilizamos várias funções desde que iniciamos este curso:
- print()
- len()
- max()
- min()
- count()
e muitas outras;
"""

from random import random

# Exemplo de utilização de funções:
"""
cores = ['verde', 'amarelo', 'azul', 'branco']

# Utilizando a função integrada (Built-in) do Python print()

print(cores)

curso = 'Programação em Pyhton: Essencial'

print(curso)

cores.append('roxo')

print(cores)

# curso.append('Mais dados...')  # AtributeError

cores.clear()
print(cores)
"""

# Mas então como definir Parâmetros

"""
Em Python, a forma geral de definir uma função é:

def nome_da_funcao(parametros_de_entrada):
    bloco_da_funcao

Onde:

nome_da_função com letras minúsculas, e se for nome composto, separado por underline (Snake Case);
parametros_de_entrada -> Opicionais, onde tendo mais de um, cada um separado por vírgula, podendo ser opcionais ou não;
bloco_da_função -> Também chamado de corpo da função ou implementação, é onde o processamento da função acontece.
Neste bloco, pode haver ou não retorno da função.

Obs: Veja que para definir uma funcao, utilizamos a palavra reservada 'def' informando ao Python que estamos definindo
uma função. Também abrimos o bloco de código com o já conhecido dois pontos : que é utilizando em Python para definir 
blocos.    
"""


# Definindo a primeira função
"""
def dizer_oi():
    print('Oi!')

"""
"""
Obs:

1 - Veja que dentro das nossas funções podemos utilizar outras funções;
2 - Veja que nossa função só executa uma tarefa, ou seja, a única coisa que ela faz é dizer oi;
3 - Veja que esta função não recebe nenhum parâmetro de entrada;
4 - Veja que esta função não tem nenhum retorno;
"""

# Utilizando funções

# Chamada de execução
"""
dizer_oi()
"""
"""
ATENÇÂO:

Nunca esqueça de utilizar o parenteses ao executar uma função

Exemplo:

# Errado
dizer_oi

# Certo
dizer_oi()

# Errado
dizer_oi ()
"""
"""
# Exemplo 2
def cantar_parabens():
    print('Parabéns para você')
    print('Nesta data querida')
    print('Muitas felicidades')
    print('Muitos anos de vida')
    print('Viva ao aniversariante!')

cantar_parabens()

# Em Python, podemos inclusive criar variáveis do tipo de uma função e executar nesta função através da variável

cantar = cantar_parabens()

cantar
print(type(cantar))

"""
"""
Funções com Retorno

"""

"""
# Existe ou não retorno

# Obs : Em Python, quando uma função não retorna nenhum valor, o retorno é "None"

numeros = [1, 2, 3]

ret_pop = numeros.pop()  # Tem retorno

print(f'Retorno de pop {ret_pop}')

ret_pr = print(numeros)  # Não retorno

print(f'Retorno de print: {ret_pr}')
"""

# Obs : Funções Python que retornam valores devem retornar esses valores com a palavra reservada return
"""
def quadrado_de_7():
    return 7 * 7

ret = quadrado_de_7()

print(f'Retorno {ret}')
"""
# Obs : Não precisamos necessariamente criar uma variável para receber o retorno de uma função. Podemos passar
# a execução da função para outras funções.
"""
def quadrado_de_7():
    return 7 * 7

print(f'Retorno {quadrado_de_7()}')
"""

# Refatorando a primeira função
"""
def dizer_oi():
    return 'Oi '

alguem = 'Pedro'

print(dizer_oi() + alguem + '!')
"""

# Obs : Sobre a palavra reservada return

# Exemplo 1
# Ela finaliza a função, ou seja, ela sai da execução da função;

"""
def dizer_oi():
    print('Estou sendo executado antes do retorno...')
    return ('Oi!')
    print('Estou sendo executado após o retorno...')  # Nunca será executado

print(dizer_oi())
"""

# Exemplo 2
# Podemos ter em uma função, diferentes returns;
"""
def nova_funcao():
    variavel = True
    if variavel:
        return 4
    elif variavel is None:
        return 3.2
    return 'b'

print(nova_funcao())
"""
# Exemplo 3
# Podemos, em uma função retornar qualquer tipo de dados e até mesmo múltiplos valores;
"""
def outra_funcao():
    return 2, 3, 4, 5

# num1, num2, num3, num4 = outra_funcao()
# print(num1, num2, num3, num4)

print(outra_funcao())
print(type(outra_funcao()))  # Tupla
"""

# Criando uma função para jogar a moeda
# Uso da biblioteca random (início do arquivo)
"""
def jogar_moeda():
    # Gera um número pseudo-randômico entre 0 e 1
    if random() > 0.5:
        return 'Cara'
    return 'Coroa'

print(jogar_moeda())
"""

# Erros comuns de condificação desnecessária.
"""
def eh_impar():
    numero = 5
    if numero % 2 != 0:
        return True
    else:  # Não necessário, vide exemplo jogar_moeda
        return False 

print(eh_impar())    
"""

"""
Funções com Parâmetro (de entrada)

- Funções que recebem dados para serem processados dentro da mesma

- Se agente pensar em um programa qualquer, geralmente temos:
enrada -> processamento -> saída

Se agente pensar em uma função ja sabemos que temos funções que:
- Não possuem entrada
- Não possuem saída
- Possuem entrada mas não possuem saída
- Não possuem entrada mas possuem saída
- Possuem entrada e saída
"""

# Refatorando uma função quadrado_de_7
"""
def quadrado_de_7():
    return 7 * 7

print(quadrado_de_7())
"""
"""
def quadrado(numero):
    # return numero * numero
    return numero ** 2  # Elevado ao quadrado ao cubo ** 3

print(quadrado(7))

ret = quadrado(6)
print(ret)

print(quadrado()) # TypeError obrigatório informar um dado para o parêmetro

"""

# Refatorando a função cantar_parabens

"""
def cantar_parabens(aniversariante):
    print('Parabéns para você')
    print('Nesta data querida')
    print('Muitas felicidades')
    print('Muitos anos de vida')
    print(f'Viva o(a) {aniversariante}!')

cantar_parabens('Patricia')
"""

# Funções pode ter n parametros de entrada. Ou seja, podemos receber como entrada
# em uma função quantos parametros forem necessários. Eles são separados por virgula.
"""
# Exemplo

def soma(a, b):
    return a + b

def multiplica(num1, num2):
    return num1 * num2

def outra(num1, b, msg):
    return (num1 + b) * msg

print(soma(2, 5))
print(soma(10, 20))

print(multiplica(4, 5))
print(multiplica(2, 8))

print(outra(3 ,2, 'Geek '))

# Obs: Se for informado um número errado de paramêtros ou argumentos, teremos um TypeError

print(soma(2, 5, 3)) # TypeError - Pasando argumentos a mais
print(soma(2)) # TypeError - Pasando argumentos a menos

"""

# Nomeando parâmetros
"""
# def nome_completo(string1, string2): seja mais objetivo como na redefinição abaixo
def nome_completo(nome, sobrenome):
    return f'Seu nome completo é {nome} {sobrenome}'

print(nome_completo('Carlos Alberto', 'Almeida Rodrigues'))
"""

# A diferença entre Parâmetros e Argumentos
"""
- ParÂmetros são variáveis declaradas na definição de uma função;
- Argumentos são dados passado durante a execução de uma função;
"""


# A ordem dos parâmetros importa
"""
nome = 'Felicity'
sobrenome = 'Smoke'

print(nome_completo(sobrenome, nome))
"""

# Argumentos nomeados (Keyword Arguments)

# Caso utilizemos nomes dos parâmetros os argumentos para informá-los, podemos utilizar qualquer ordem
# A partir da sua utilização, pode se usar qualquer ordem nos parâmetros

"""
print(nome_completo(nome='Agelina', sobrenome='Jolie'))
print(nome_completo(sobrenome='Jolie', nome='Agelina'))
"""

# Erro comum na utilização do return


def soma_impares(numeros):
    total = 0
    for num in numeros:
        if num % 2 != 0: # Módulo de 2 é diferente de 0?
            total = total + num
        # return total - Local errado, término inesperado da função
    return total # Local correto


if __name__ == '__main__':
    lista = [1, 2, 3, 4, 5, 6, 7]
    print(soma_impares(lista))

    tupla = (1, 2, 3, 4, 5, 6, 7)
    print(soma_impares(tupla))

# Funções com parâmetro padrão (Default Parameters)
 
# Funções onde a passagem de parâmetro seja opicional
 
# Porque utilizar? Funções mais flexiveis, menos erros com parâmetros incorrentos, código mais legível

# Exemplo de função onde a passagem de parâmetros é opcional
"""
print('Geek University')
print()
"""


# Exemplo de função onde a passagem de parâmetros é opcional
"""
# Obrigatória
def quadrado(numero):
    return numero ** 2

print(quadrado(2))
print(quadrado())  # Type Error

# Opcional

def exponencial(numero, potencia=2):
    return numero ** potencia


print(exponencial(2, 3))  # 2 * 2 * 2 = 8
print(exponencial(3, 2))  # 3 * 3 = 9

print(exponencial(3))  # Por padrão ele ao quadrado
print(exponencial(3, 5))  # Eleva a potência informada pelo usuário

# Obs
# Se o usuário passar somente 1 argumento, este será atribuido ao parâmetro número, e será o quadrado por padrão
# Se o usuário passar 2 argumentos, o primeiro sera atribuido a parametro numero e o segundo ao parametro potencia,
# então será calculada esta potência;

"""

# OBS: Em funções Pythin, os parÂmetros com valores default DEVEM sempre estar ao final da declaração.

"""
# ERRO!
def teste(num=2, potencia):
    return num ** potencia

print(teste(6))
"""

# Outros exemplos
"""

def soma(num1, num2):
    return num1 + num2


print(soma(4, 3))
print(soma(4))  # TypeError
print(soma())  # TypeError
"""

# Exemplo mais complexo

"""
def mostra_informacao(nome='Geek', instrutor=False):
    if nome == 'Geek' and instrutor:
        return 'Bem vindo instrutor Geek'
    elif nome == 'Geek':
        return 'Eu pensei que você era o instrutor'
    return f'Olá {nome}'

print(mostra_informacao())
print(mostra_informacao(instrutor=True))  # Simplesmente passando só true, seria considerado um nome
print(mostra_informacao('Calos'))
print(mostra_informacao('Angelina'))
"""

# Quais tipos de dados podemos utilizar como valores default para parâmetros?

# Qualquer tipo: Número, strings, floats, booleanos, listas, tuplas, dicionários, funções e etc;

# Exemplo de parâmetro padrão do tipo função

"""
def soma(num1, num2):
    return num1 + num2

def mat(num1, num2, fun=soma):
    return fun(num1, num2)

def subtracao(num1, num2):
    return num1 - num1

print(mat(2, 3))
print(mat(2, 2, subtracao))  # Neste caso a função é passada sem parâmetros

"""

# Escopo - Evitar problemas e confusões

# Variáveis Globais
# Variáveis Locais

"""
instrutor = 'Geek'  # Variável global

def diz_oi():
    instrutor = 'Python'  # Variável local se sobrepoe e variável Global
    return f'Oi {instrutor}'

print(diz_oi())
"""

# OBS: Se tivermos uma variável local com o mesmo nome de uma variável global, a local terá preferência
"""

def diz_oi():
    prof = 'Geek'  # Variável local
    return f'Olá {prof}'


print(diz_oi())
print(prof) # NameError
"""

# Atenção com variáveis globais (Se puder evitar, evite!)
"""
total = 0


def incrementa():
    total = total + 1  # UnboundLocalError : A variável local está sendo utilizada para processamento sem ter sido inicializada.
    return total

print(incrementa())

"""

# Forma correta
"""
total = 0


def incrementa():
    global total  # Avisando que queremos utilizar a variável global
    total = total + 1
    return total


print(incrementa())
print(incrementa())
print(incrementa())
"""

# Podemos ter funções que são declaradas dentro de funções, e também tem uma forma especial de escopo de variável
"""

def fora():
    contador = 0

    def dentro():
        nonlocal contador  # Indicando que não é nem a variável local e nem global, e sim da função pai
        contador = contador + 1
        return contador
    return dentro()


print(fora())
print(fora())
print(fora())

print(dentro())  # NameError
"""







