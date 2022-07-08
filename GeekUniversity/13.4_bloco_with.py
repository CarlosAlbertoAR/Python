"""
O bloco with

# Fluxo de trabalho com os arquivos

 1 - Abrir com open()
 2 - Manipular com read(), readlines() etc
 3 - Fechar o arquivo com close() -> o bloco with dispensa este último

O bloco with é utilizado para se criar um contexto de trabalho, onde os recursos utilizados são fechados após o bloco with

"""

# Bloco with - Forma Pythônica de manipular arquivos

with open('texto.txt') as arq:
    print(arq.readlines())
    print(arq.closed)

# print(arq.read())  # ValueError: I/O operation on closed file.

print(arq.closed)  # Já fechado
