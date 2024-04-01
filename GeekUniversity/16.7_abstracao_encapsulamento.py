"""
POO - Abstração e Encapsulamento

O grande objetivo da POO é encapsular nosso código dentro de um grupo lógico e hieráquico utilizando classes.

Encapsular -> cápsula


                Classe
--------------------------------------
/                                    /
/         Atributos e métodos        /
/                                    /
-------------------------------------

# Relembrando Atributos/Métodos privados em Python

Imagine que temos uma classe chamada Pessoa, contendo um atributo privado chamado __nome e um métofo privado chamado
__falar()

Esses elementos privados só devem/deveriam ser acessados dentro da classe. Com Python acontece um fenômeno chamado
Name Mangling, que faz uma alteração na forma de se acessar os elementos privados, conforme:

_Classe__elemento

Exemplo - Acessando elementos privados fora da classe:

instancia._Pessoa__nome

instancia._Pessoa__falar()


Abstração em POO, é o ato de expor apenas dados relevantes de uma classe, escondendo atributos e métodos privados de
usuário.

"""

class Conta:

    contador = 400

    def __init__(self, titular, saldo, limite):
        self.numero = Conta.contador
        self.titular = titular
        self.saldo = saldo
        self.limite = limite
        Conta.contador += 1

    def extrato(self):
        print(f'Saldo de {self.saldo} do titular {self.titular} com limite de {self.limite}')

    def depositar(self, valor):
        self.saldo += valor

    def sacar(self, valor):
        self.saldo -= valor


# Testando

conta1 = Conta('Geek', 150.00, 1500)

print(conta1.numero)
print(conta1.titular)
print(conta1.saldo)
print(conta1.limite)

# Alteração que não deveria ser permitida

conta1.numero = 42
conta1.titular = 'Xuxa'
conta1.saldo = 999999999999999999999
conta1.limite = 999999999999999999999999999999

print(conta1.__dict__)


# Refatorando a classe com encapsulamento, aproveitando e inseriondo validações

class Conta:

    contador = 400

    def __init__(self, titular, saldo, limite):
        self.__numero = Conta.contador
        self.__titular = titular
        self.__saldo = saldo
        self.__limite = limite
        Conta.contador += 1


    def extrato(self):
        print(f'Saldo de {self.saldo} do titular {self.titular} com limite de {self.limite}')


    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
        else:
            print('O valor de depósito precisa ser positivo')

    def sacar(self, valor):
        if self.__saldo >= valor:
            self.__saldo -= valor
        else:
            print('Saldo insuficiente')


# Testando novamente


conta1 = Conta('Geek', 150.00, 1500)

print(conta1.__dict__)

conta1.depositar(-150)

print(conta1.__dict__)

conta1.sacar(200)

print(conta1.__dict__)


conta1 = Conta('Angelina', 150.00, 1500)
print(conta1.__dict__)

conta2 = Conta('Felicity', 300.00, 2000)
print(conta1.__dict__)

valor = 100


