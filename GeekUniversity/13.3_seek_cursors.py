"""
Seek e Cursors

seek() -> É usada para movimentar o cursor pelo arquivo.

# Quando abrimos um arquivo com a função open() é criada uma conexão (streaming) entre o arquivo no disco do computaor e o seu
# programa. Ao finalizar o processamento com o arquivo, deve se fechar a conexão com a função close()

# Fluxo de trabalho com os arquivos

 1 - Abrir com open()
 2 - Manipular com read(), readlines() etc
 3 - Fechar o arquivo com close()

 Testar se está fechado
 closed()

OBS: Ao tentar usar um arquivo fechado (closed) será retornado um ValueError : I/O operation on closed file.
"""

arquivo = open('texto.txt')

# print(arquivo.read())

# seek -> recebe um parâmetro que indica onde queremos colocar o cursor
# Movimentando o cursor pelo arquivo com a função seek()

# Volta o cursor para a posição zero
"""
arquivo.seek(0)

# Imprimindo novamente

print(arquivo.read())
"""

# Voltando o cursor para a posição 21 e imprimindo em diante
"""
arquivo.seek(22)

print(arquivo.read())
"""

# Função para ler o arquivo linha a linha
"""
ret = arquivo.readline()

print(type(ret))

print(ret.split(' ')) # Imprimindo em lista
"""

# readlines() -> Lê e insere cada linha como um item de uma lista
"""
linhas = arquivo.readlines()

print(linhas)

print(len(linhas))
"""

# read














