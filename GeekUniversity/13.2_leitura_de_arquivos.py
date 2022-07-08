"""
Leitura de arquivos

Para ler o conteúdo de um arquivo em Python, utilizamos a função integrada open(), que literalmente significa 'abrir'

open() -> A forma mais simples de utilização nós passamos apenas um parâmeto de entrada, que neste caso é o nome do
arquivo a ser lido, esta função retorna um _io.textIOWraper e é com ele que trabalhamos então

<_io.TextIOWrapper name='texto.txt' mode='r' encoding='cp1252'>

name='texto.txt' -> Nome do arquivo
mode r -> Modo Leitura -> r (read)
encoding='cp1252' -> Codificação

# O Ptyhon utiliza um recurso para trabalhar com arquivos chamado cursor. Esse cursor funciona como o cursor do teclado
# quando estamos escrevendo ou navegando

"""

# https://docs.python.org/3/library/functions.html#open

# OBS: Por padrão, a função open() abre o arquivo para leitura. Caso não exista, teremos o erro FileNotFoundError

# Abrindo e imprimindo os detalhes do arquivo
arquivo = open('texto.txt')

print(arquivo)

print(type(arquivo))

# Para ler o conteúdo de um arquivo após a sua abertura devemos utilizar a função read()
print(arquivo.read())

ret = arquivo.read()

print(type(ret))

# Lendo uma quantidade fixada de caracters

print(arquivo.read(50))



