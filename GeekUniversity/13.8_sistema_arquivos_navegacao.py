"""
Sistema de arquivos e navegação

Paa fazer uso de manipulação de arquivos do sistema, precisamos importar e fazer uso do múdulo "os".:key

os - Operating System - Sistema Operacional


"""

import os

# getcwd - REtorna o Current Work Directory - Diretório de trabalho corrente
# Retorna o path (caminho) absoluto
"""
print(os.getcwd())
"""

# Para mudar o diretório, podemos usar o chdir()
"""
os.chdir('..')

print(os.getcwd())
"""

# Podemos checar se um diretório é absoluto ou relativo
"""
print(os.path.isabs('E:\Python\GeekUniversity'))  # True

print(os.path.isabs('Python\GeekUniversity'))  # False
"""

# OBS : para usuários Windows, terá que ter cuidado ao verificar diretórios
"""
print(os.path.isabs('E:\\Python\\GeekUniversity'))
"""

# Podemos identificar o Sistema Operacional com o módulo os
"""
print(os.name)  # posix (Linux e Mac), nt (Windows)
"""

# Podemos ter mais detalhes no Sistema Operacional

# print(os.uname())  # Possix

# import sys # Windows
# print(sys.platform)

# Acessar um diretório
# Veja que os.path.join() recebe 2 parametros, sendo o 1 - O diretório base e o 2 - O diretório que seja juntado
"""
print(os.getcwd())  # E:\Python\GeekUniversity

newdir = os.path.join(os.getcwd(), 'geek')

os.chdir(newdir)

print(os.getcwd())  # E:\Python\GeekUniversity\geek
"""

# Listando arquivos e diretórios com o listdir()
"""
print(os.listdir())  # Retorna uma lista iterável
"""

# Lista arquivos e diretórios com mais detalhes com scandir()
# OBS: Quando utilizada, a função scandir(), é necessário dfechá-la, assim como quando abrimos arquivos texto.

scannner = os.scandir()

arquivos = list(scannner)

scannner.close()

print(arquivos[0].inode())  # Nome do arquivo
print(arquivos[0].is_dir())  # É uma diretório ?
print(arquivos[0].is_file())  # É um arquivo ?
print(arquivos[0].is_symlink())  # É um link simbólico ?
print(arquivos[0].name)  # Nome do arquivo
print(arquivos[0].path)  # Caminho até do arquivo, apartir do diretório atual
print(arquivos[0].stat())  # ?







