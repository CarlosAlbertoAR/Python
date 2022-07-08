"""
Recebendo dados do usuário

dir(__builtins__) > Recursos integrados da linguagem, entre eles "input"

input() -> todo dado recebido via input é do tipo String

Em Python, string é tudo que estiver entre:

- Aspas simples; ex: 'Angelina jolie' 
- Aspas duplas; ex: "Angelina Jolie"
- Aspas simples triplas; ex : '''Angelina Lolie'''
"""
# Aspas duplas triplas; ex: """Angelina Jolie"""
 
# Entrada de dados
# print("Qual seu nome?")
# nome = input()  # Input -> Entrada pelo teclado

nome = input("Qual o seu nome?")

# Exemplo de print 'antigo' 2.x
# print("Seja bem vindo(a) %s" % nome)

# Exemplo de print 'moderno' 3.x
# print("Seja bem vindo(a) {0}".format(nome))

# Exemplo de print 'mais atual' > 3.7
print(f"Seja bem vindo(a) {nome}")

# print("Qual a sua idade? ")
# idade = input()

idade = int(input("Qual a sua idade? "))

# Processamento

# Saida
# Exemplo de print 'antigo' 2.x
# print("%s tem %s anos" % (nome, idade))

# Exemplo de print 'moderno' 3.x
# print("{0} tem {1} anos".format(nome, idade))

# Exemplo de print 'mais atual' > 3.7
print(f"{nome} tem {idade} anos")

"""
int(idade) => cast

Cast é a 'conversão' de um tipo de dados par outro.
"""

print(f'e nasceu em {2020 - idade}')
