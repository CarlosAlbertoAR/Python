"""
Sistema de Arquivos - Manipulação

https://docs.python.org/3/library/os.html
"""
import os

# Descobrindo se um arquivo ou diretório existe

# Arquivo
"""
print(os.path.exists('arquivo.txt'))  # False
print(os.path.exists('texto.txt'))  # True
"""

# Diretorio - Paths relativos
"""
print(os.path.exists('geek'))  # True
print(os.path.exists('geek/university'))  # True
print(os.path.exists('geek/university/modulo3.py'))  # True
print(os.path.exists('outro'))  # False
"""

# Diretorio - Paths absolutos
"""
print(os.path.exists('E:\\Python\\GeekUniversity\\geek'))  # True
print(os.path.exists('E:\\Python\\GeekUniversity\\geek\\modulo1.py'))  # True
"""

# Criando arquivos
# OBS: Se utilizado no Mac OS, pode haver um erro de PermissionError
# OBS: Se Criando um arquivo e já existir, haverá um erro FileExistsError
"""
# Forma 1 
open('arquivos_teste.txt', 'w').close()

# Forma 2
open('arquivos_teste2.txt', 'a').close()

# Forma 3
with open('arquivo_teste3.txt', 'w') as arquivo:
    pass
    
# Forma mais indicada

os.mknod('arquivo_teste4.txt')
os.mknod('E:\\Python\\GeekUniversity\arquivo_teste4.txt')
"""

# Criando diretórios - únicos
# OBS : A função cria o diretório, e caso ja exsita, haverá um erro FileExistsErro
# Se tentar criar um diretório em path não autorizado PermissionError
"""
os.mkdir('templates')
os.mkdir('E:\\Python\\GeekUniversity\\templates')
"""

# Criando diretórios - multiplos
"""
os.makedirs('E:\\Python\\GeekUniversity\\newdir1\\newdir2\\newdir3')

os.makedirs('E:\\Python\\GeekUniversity\\newdir1\\newdir2\\newdir3', exist_ok=True)  # Ignora se já existir as pastas
"""

# Renomeando diretórios
# OBS: Se o diretório não existir, teremos um FileNotFoundError
# OBS: Se o diretório que se quer renomear, estiver vazio, haverá um OSError
"""
os.rename('geek', 'geek2')
"""

# Reanomeando arquivos

# os.rename('geek/university/modulo3.py', 'geek/university/modulo99.py'

# Deletar arquivos
# OBS : ATENÇÃO! Tome cuidado com o comandos de deleção. Os arquivos não vão para lixeira, são deletados definitivamente
# Podendo usar o módulo de terceiros "sendtotrash"
# OBS: Se você estiver no Windows e o arquivo que quiser deletar estiver em uso, haverá um erro do Windows.
# OBS: Caso o arquivo não exista, haverá um FileNotFoundError
# OBS: Se vocÊ informar ma diretório ao invés de um arquivo, haverá um IsADirectoryError
"""
os.remove('texto.txt')
"""

# Remover diretórios vazios
# OBS: Se o diretório  tiver qualquer conteúdo, teremos um OSError
# OBS: Se o diretório não existir, teremos um FileNotFoundError
"""
os.rmdir('geek')
"""

# Removendo uma árvore de Diretórios
"""
for arquivo in os.scandir('geek'):
    if arquivo.is_file():
        os.remove(arquivo.path)
"""

# Removendo uma árvore de diretórios vazios
# OBS: Se algum dos diretórios tiver arquivos ou diretórios, o processo para.
"""
os.removedirs('geek')
"""

# Trabalhando com arquivos e diretórios temporários
# Criando um diretório temporário, abrindo o mesmo e dentro dele criando um arquivo para excrever um texto. No dinal,
# usamos um input() só para mantermos os arquivos temporários 'vivos' dentro do bloco with
"""
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    print(f'Criei  o diretório temporário em {tmp}')
    with open(os.path.join(tmp, 'arquivo_temporario.txt'), 'w') as arquivo:
        arquivo.write('Geek University\n')
    input()
"""

# Criando arquivo temporário
# OBS : Em arquivos temporário só conseguimos escrever bits. Por isso o uso de b''

import tempfile

with tempfile.TemporaryDirectory() as tmp:
    tmp.write(b'Geek University\n')  # Arquivo binário
    tmp.seek(0)
    print(tmp.read)






