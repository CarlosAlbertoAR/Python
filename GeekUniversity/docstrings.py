"""
Documentando funções com Docsstrings

OBS : Podemos ter acesso a documentação de uma função em Python utilizando:

 - Help(nome_funcao)
 - print(nome_funcao.__doc__) A propriedade especial __doc__
"""

"""
print(help(print))
"""
"""
# Exemplos


def diz_oi():
    """"""Uma função simples qye retorna a string 'Oi !'"""""" (apenas 3 aspas)
    return 'Oi!'


print(help(diz_oi()))
"""
"""

def exponencial(numero, potencia=2):
    """""" (apenas 3 aspas)
    Função que retorna por padrão o quadrado de um numero ou o numero elevado a potencia informada
    :param numero: Número que desejamos elevar a potencia.
    :param potencia: Potência que queremos gerar o exponencial. Por padrão é 2.
    :return: Retorna o exponencial de numero elevado a potencia.
    """""" 
    return numero ** potencia
"""


