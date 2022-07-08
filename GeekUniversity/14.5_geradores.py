"""
Geradores

- Geradores (Generators) são Iterators (Iteradores);

OBS: O Contrário não é verdadeiro, ou seja, nem todo iterator é um generator

Outras informações:
- Generators pode ser criados com funções geradoras;
- Funções geradoras utilizam a palavra reservada yield;
- Generators pode sr acriados com Expressões Geradoras;

Diferenças entre funções e Generator Functions (Funções Geradoras)

----------------------------------------------------------------------------------
/ Funções                               / Generator Functions                    /
----------------------------------------------------------------------------------
/ utilizam return                       / utilizam yield                         /
----------------------------------------------------------------------------------
/ retorna uma vez                       / podem utilizar yield múltiplas vezes   /
----------------------------------------------------------------------------------
/ quando executads, retorna valor       / quando executada, retorna um generator /
----------------------------------------------------------------------------------
"""

# Exemplo de Função Geradora (Generator Function)

def conta_ate(valor_maximo):
    contador = 1
    while contador <= valor_maximo:
        yield contador  # Retorna o valor, porém não sai da função, aguarda o comando next() para então retornar outro
        contador = contador + 1

# OBS: Uma Generator Function não é um Generator, ela gera um generator, ok?


# Usando com next()
"""
gen = conta_ate(5)

print(type(gen))  # <class 'generator'>

print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
"""

# Usando com For
"""
gen = conta_ate(5)

print(next(gen))  # 1

for num in gen:  # 2, 3, 4, 5
    print(num)
"""

# Gerando os resultados de uma única vez

gen = list(conta_ate(5))

print(gen)
