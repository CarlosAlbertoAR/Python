"""
Escrevendo um iterador customizado

Ele precisa ter pelo menos duas funções: iter() e next() implementadas com dunder

"""

# Classe Contador que terá comportamento similar ao do range

class Contador:
    def __init__(self, menor, maior):
        self.menor = menor
        self.maior = maior

    def __iter__(self):  # Vai ser chamado internamente pelo for
        return self

    def __next__(self):  # Vai ser executado internamento pelo for
        if self.menor < self.maior:
            numero = self.menor
            self.menor = self.menor + 1
            return numero
        raise StopIteration


# Utilizando

for n in Contador(1, 61):
    print(n)
