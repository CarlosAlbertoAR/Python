"""
Escopo de variáveis

Dois casos de escopo:

1 - Variáveis globais;
   - São reconhecidas, ou seja seu escopo compreende todo o programa.

2 - Variáveis locais;
    - São reconhecidas apenas no bloco onde foram declaradas, ou seja,
    seu escopo está limitado ao bloco onde foi declarada

Para declarar variaceis em Python fazemos:

nome_da_variavel = valor_da_variavel

Python é uma linguagem de tipagem dinâmica. Isso significa que
ao declararmos uma variável, nós não colocamos o tipo de dado dela.
Este tipo é inferido ao atribuirmos o valor a mesma

Exemplo em C:
int numero = 42;

Exemplo em Java
int numero = 42;

"""

# Exemplo de variável global
numero = 42
print(numero)
print(type(numero))

# Reatribuição
numero = 'Geek'
print(numero)
print(type(numero))

numero = 42
# novo = 0

if numero > 10:
    novo = numero + 10  # A variável novo está declarada localmente dentro do bloco do if. Portanto é local
    print(novo)

print(novo)
