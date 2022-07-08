"""
StringIO

ATENÇÃO: Para ler ou escrever dados em arquivos do sistema operaciona, o software precisar ter premissão de leitura e
escrita no diretório pretendido

StringIO -> Utilizado para ler e criar arquivos em memória.

"""

# Primeiro é necessário o import

from io import StringIO

mensagem = 'Esta é apenas uma string normal'

# Podemos criar um arquivos em memória já com uma strinf inserida ou mesmo vazrio para inserirmos texto depois

arquivo = StringIO(mensagem)  # Equivalente a arquivo = open('arquivo.txt', 'w')

# Agora tendo o arquivo, podemos utilizar tudo que já sabemos

print(arquivo.read())

# Escrevendo outros textos
arquivo.write('\nInserindo outro texto')

# Podemos inclusive movimentar o cursor
arquivo.seek(0)

print(arquivo.read())

