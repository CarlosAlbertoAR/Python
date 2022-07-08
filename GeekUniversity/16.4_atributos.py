"""
POO - Atributos

Atributos -> Representam as características do objeto. Ou seja, pelos atributos nós conseguimos representar
computacionalmente os estados de um objeto.

OBS: Em Python, por convenção, ficou definido que todo atributo de uma classe é público. Ou seja, pode ser acessado em
todo o projeto.
Caso queiramos demonstrar que determinado atributo deve ser tratato como privado (acessado somente dentro da própria
classe), utiliza-se __ duplo underscore no início do seu nome.

Isso é cpmhecido também como Name Mangling


Em Python, dividimos os atributos em 3 grupos:
    - Atributos de Instância;
    - Atributos de Classe;
    - Atributos Dinâmicos;

# Atributos de instância: São declarados dentro do método construtor.

OBS : Método construtor: É um método especial utilizado para a construção do objeto.
"""

# Em Java, uma classe Lâmpada, incluindo seus atributos ficaria mais ou menos assim:
"""
public class Lampada(){
    private int voltagem;
    private String cor;
    private Boolean lidada = false;

    public Lampada(int voltagem, String cor){
        this.voltagem = voltagem
        this.cor = cor;
    }
    
    public int getVoltagem(){
        :return this.voltagem;
    }    
}
"""

# Em Python a mesma classe


class Lampada:

    def __init__(self, voltagem, cor):
        self.voltagem = voltagem
        self.cor = cor
        self.ligada = False


# Outras Classes com atributos de instância públicos


class ContaCorrente:

    def __init__(self, numero, limite, saldo):
        self.numero = numero
        self.limite = limite
        self.saldo = saldo


class Produto:

    def __init__(self, nome, descricao, valor):
        self.nome = nome
        self.descricao = descricao
        self.valor = valor


class Usuario:

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


# Classe com atributos de instância privados

class Acesso:

    def __init__(self, email, senha):
        self.__email = email
        self.__senha = senha

    def mostra_senha(self):
        return self.__senha

    def mostra_email(self):
        return self.__email

# OBS: Lembre que isso é apenas uma convenção, ou seja, a linguagem não irá impedir que façamos acesso aos atributos
# sinalizados como privados fora da classe.

# Exemplo


user = Acesso('user@gmail.com', '123456')

# print(user.email)  # AttributeError

# print(user.__senha)  # AttributeError

print(user._Acesso__senha)  # Temos acesso, mas não deveríamos fazer este acesso.

print(user.mostra_senha())


# Afinal o que são atributos de instância?
# Significa que ao criarmos instâncias/objetos de uma classe, todos as intâncias terão estes atributos

user1 = Acesso('user@gmail.com', '123456')
user2 = Acesso('user@hotmail.com', '654321')

print(user1.mostra_email())
print(user2.mostra_email())


# Atributos de Classe
# São atributos que são declarados diretamente na Classe, ou seja, fora do construtor. Geralmente já inicializamos um
# valor, e este valor é compartilhado entre todas as instâncias da classe, ou seja ao invés de cada instância da classe
# ter seu próprios valores como é o caso dos atributos de instância, com os atributos de classe todas as intâncias terão
# o mesmo valor para este atributo.

# Refatorando a classe produto


class Produto:

    # Atributo de classe
    imposto = 1.05  # 0.05% de imposto
    contador = 0  # Contador que pode ser icrementado e utilizado para acumular contagem, instânciados apenas 1 vez

    def __init__(self, nome, descricao, valor):
        self.id = Produto.contador + 1
        self.nome = nome
        self.descricao = descricao
        self.valor = (valor * Produto.imposto)
        Produto.contador = self.id


p1 = Produto('PS4', 'Video Game', 2300)
p2 = Produto('Xbos S', 'Video Game', 4500)

print(p1.valor)  # Acesso possível, mas incirreto de um atributos de classe
print(p1.id)
print(p2.valor)  # Acesso possível, mas incirreto de um atributos de classe
print(p2.id)

# OBS: Não precisamos criar uma instância de uma classe para fazer acesso a um atributo de classe

print(Produto.imposto)  # Acesso correto de um atributo de classe

# OBS: Em linguagens como Java, os atributos conhecidos como atributos de casse em Pythom, são chamados de atributos
# estáticos.


# Atributos Dinâmicos
# É um atributo de instância que pode ser criado em tempo de execução.
# OBS: O atributo dinâmico será exclusivo da instância que o criou.

p1 = Produto('PS4', 'Video Game', 2300)

p2 = Produto('Arroz', 'Mercearia', 5.99)

# Criando um atributo dinâmico em tempo de execução

p2.peso = '5kg'  # Note que na classe produto não existe o atributo peso

print(f'Produto: {p2.nome}, Descrição: {p2.descricao}, Valor: {p2.valor}, Peso: {p2.peso}')

# Deletanto atributos

print(p1.__dict__)
print(p2.__dict__)

del p2.peso
del p2.valor

print(p1.__dict__)
print(p2.__dict__)





