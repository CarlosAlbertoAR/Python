"""
Estruturas lógicas: and(e), or (ou), not (não), is (é)

Operadores unários:
    - not
Operadores binários:
   - and, or, is

"""

ativo = True
logado = False

# Para o 'and', ambos os valores precisam ser True;
if ativo and logado:
    print('_and_ Bem-vindo usuário!')
else:
    print('_and_ Você precisa ativar a sua conta. Por favor, cheque seu e-mail')

# Para o 'or', um ou outro valor precisa ser True;
if ativo or logado:
    print('_or_ Bem-vindo usuário!')
else:
    print('_or_ Você precisa ativar a sua conta. Por favor, cheque seu e-mail')

# Para o 'not', o valor do booleano é invertido, ou seja, se for true, vira False, se for False, vira True;
if not ativo:
    print('_not_ Você precisa ativar a sua conta. Por favor, cheque seu e-mail')
else:
    print('_not_ Bem-vindo usuário')

# Para o 'is', o valor é comparado com um segundo.
if ativo is False:
    print('_not_ Você precisa ativar a sua conta. Por favor, cheque seu e-mail')
else:
    print('_not_ Bem-vindo usuário')

print(ativo is False)