"""
POO - Métodos

- Métodos (funções) -> Representam os comportamentos do objeto. Ou seja, as ações que este objeto pode realizar no seu
sistema.

Em Python, dividimos os métodos em 2 grupos:
    - Métodos de instância
    - Métodos de Classe.

# Métodos de Instância

# O método dunder init __init__ é um método especial chamado de construtor e sua função é construir o objeto a partir da
classe.

OBS : Todo elemento em Python que inicia e finaliza com duplo underline é chamado de dunder (double underline)

OBS : OS métodos/funções em Python com dunder são chamados de métodos mágicos.

ATENÇÃO! Por mais que possamos criar nossas próprias funções utilizando dunder, não é aconselhado. Python possui vários
métodos com essa forma de nomeclatura e pode ser que mudemos o comportamento dessas funçãoes mágicas internas da
linguagem. Então evite ao máximo, de preferência nunca o faça.

Métodos são escritos em letras minúsculas. Se o nome for composto terá as palavras separados por underline.

Métodos de classe em Python são conhecidos como métodos estáticos em outras linguagens.

"""


class Lampada:

    def __init__(self, cor, voltagem, luminosidade):
        self.__cor = cor
        self.__voltagem = voltagem
        self.__luminosidade = luminosidade


class ContaCorrente:

    contador = 4999

    def __init__(self, numero, limite, saldo):
        self.__numero = ContaCorrente.contador + 1
        self.__limite = limite
        self.__saldo = saldo
        ContaCorrente.contador = self.__numero


class Produto:

    contador = 0

    def __init__(self, nome, descricao, valor):
        self.id = Produto.contador + 1
        self.__nome = nome
        self.__decricao = descricao
        self.__valor = valor
        Produto.contador = self.id

    def desconto(self, porcentagem):
        """ Retorna o valor do produto com o desconto """
        return (self.__valor * (100 - porcentagem)) / 100

from passlib.hash import pbkdf2_sha256 as cryp


class Usuario:

    contador = 0

    def __init__(self, nome, sobrenome, email, senha):
        self.__id = Usuario.contador + 1  # Métodos públicos
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__email = email
        self.__senha = cryp.hash(senha, rounds=200000, salt_size=16)
        Usuario.contador = self.__id

    def nome_completo(self):
        return f'{self.__nome} {self.__sobrenome}'

    def checa_senha(self, senha):
        if cryp.verify(senha, self.__senha):
            return True
        return False


"""
p1 = Produto('PS4', 'Video Game', 2300)

print(p1.desconto(10))
"""

"""
user1 = Usuario('Angelina', 'Jolie', 'angelina@gmail.com', '123456')
user2 = Usuario('Felicity', 'Jones', 'felicity@gmail.com', '654321')

print(user1.nome_completo())
print(Usuario.nome_completo(user1))

print(user2.nome_completo())

print(f'Senha: {user1._Usuario__senha}')  # Acesso de forma errada de atributo de classe
print(f'Senha: {user2._Usuario__senha}')  # Acesso de forma errada de atributo de classe
"""

""" Uso da classe Usuario e criptografia

nome = input('Informe o nome: ')
sobrenome = input('Informe o sobrenome: ')
email = input('Informe o email: ')
senha = input('Informe a senha: ')
confirma_Senha = input('Confirme a senha: ')

if senha == confirma_Senha:
    user = Usuario(nome, sobrenome, email, senha)
else:
    print('Senha não confere')
    exit(42)

print('Usuário criado com sucesso!')

senha = input('Informe a senha para acesso: ')

if user.checa_senha(senha):
    print('Acesso permitido')
else:
    print('Acesso negado')

print(f'Senha User criptografada: {user._Usuario__senha}')  # Acesso errado
"""

# Métodos de Classe

"""
class Usuario:

    contador = 0

    @classmethod  # Método de Classe, usa-se um decorator, o self vira cls (a própria classe)
    def conta_usuarios(cls):
        print(f'')
        print(f'Temos {cls.contador} usuários no sistema')

    def __init__(self, nome, sobrenome, email, senha):
        seçf.__id = Usuario.contador + 1
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__email = email
        self.__senha = cryp.hash(senha, rounds=200000, salt_size=16)
        Usuario.contador = self.__id

    def nome_completo(self):
        return f'{self.__nome} {self.__sobrenome}'

    def checa_senha(self, senha):
        if cryp.verify(senha, self.__senha):
            return True
        return False


user = Usuario('Carlos', 'Alberto', 'carlos@gmail.com', '123456')

Usuario.conta_usuarios()  # Forma correta
user.conta_usuarios()  # Possível, mas incorreta
"""

# Métodos de classe privados
"""

class Usuario:

    contador = 0

    @classmethod  # Método de Classe, usa-se um decorator, o self vira cls (a própria classe)
    def conta_usuarios(cls):
        print(f'')
        print(f'Temos {cls.contador} usuários no sistema')

    def __init__(self, nome, sobrenome, email, senha):
        self.__id = Usuario.contador + 1
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__email = email
        self.__senha = cryp.hash(senha, rounds=200000, salt_size=16)
        Usuario.contador = self.__id
        print(f'Usuário criado: {self.__gera_usuario()}')

    def nome_completo(self):
        return f'{self.__nome} {self.__sobrenome}'

    def checa_senha(self, senha):
        if cryp.verify(senha, self.__senha):
            return True
        return False

    def __gera_usuario(self):  # Método de classe privado
        return self.__email.split('@')[0]


user = Usuario('Carlos', 'Alberto', 'carlos@gmail.com', '123456')

print(user._Usuario__gera_usuario())  # Acesso de forma ruim...
"""

# Método Estático

class Usuario:

    contador = 0

    @classmethod
    def conta_usuarios(cls):
        print(f'')
        print(f'Temos {cls.contador} usuários no sistema')

    @staticmethod
    def definicao():  # Método estático, não faz acesso nem a atributos da classe nem da instância
       return 'UXR344'

    def __init__(self, nome, sobrenome, email, senha):
        self.__id = Usuario.contador + 1
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__email = email
        self.__senha = cryp.hash(senha, rounds=200000, salt_size=16)
        Usuario.contador = self.__id
        print(f'Usuário criado: {self.__gera_usuario()}')

    def nome_completo(self):
        return f'{self.__nome} {self.__sobrenome}'

    def checa_senha(self, senha):
        if cryp.verify(senha, self.__senha):
            return True
        return False

    def __gera_usuario(self):
        return self.__email.split('@')[0]


user = Usuario('Carlos', 'Alberto', 'carlos@gmail.com', '123456')

print(user.definicao())  # Acesso de forma ruim...

