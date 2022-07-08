"""
Dunfer Name e Dunder Main

Dunder -> Double Under

Dunder Name -> __name__

Dunder Main -> __main__

Em Python, são utilizados dunder para criar funções, atributos) propriedades e etc utulizando Double Under para não
gerar conflito com os nomes desse elementos na programação

# Na linguagem C, temos um programa da seguinte forma:

int main(){
    return 0;
}

# Na linguagem Java, tempos um programa daseguinte forma:

public static void main(String[] args){
}

# Em Python, se executarmos um módulo Python diretamente na linha de comando, internamente o Python atribuirá a variável
__name__ o valor __main__ indicando que este módulo é o múdulo de execução principal

"""

# Verifique em funcoes.py na linha 362, o uso de dunder
"""
from funcoes import soma_impares


print(soma_impares([1, 2, 3, 4, 5, 6]))
"""


import primeiro
import segundo

