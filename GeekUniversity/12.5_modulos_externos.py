"""
Módulos Externos

Utilizamos o gerenciados de pacotes Python chamado Pip-  Python Installer Package

https://pypi.org

Você pode conhecer todos os pacotes externos oficiais

"""

# Instalando novo módulo externo
"""
# $ pip install colorama

"""

# Colorama é um utilitário para permitir impressão de textos coloridos no terminal
"""
from colorama import init, Fore, Back

init()
print(Fore.RED + 'Geek Univertity')
print(Fore.BLUE + 'Geek Univertity')
print(Back.RED + 'Geek Univertity')
"""

# python-pdf é um utilitário para  manipular arquivos pdf
"""
import pydf

pdf = pydf.generate_pdf('<h1>Geek University</h1>')

with open('test_doc.pdf', 'wb') as f:
    f.write(pdf)
"""