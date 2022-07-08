"""
Decoredores (Decorators)

O que são decorators?

- Decorators são funções;
- Decorators envolvem outras funções e aprimoram seus comportamentos;
- Decorators também são exemplos de Higher ORder Functions;
- Decorators tem um sintaxe própria, usando "@" (Sybtatic Sugar / Açucar Sintático)

/----------------------------------------/
/         Functions Decorator            /
-----------------------------------------

/ /----------------------------------------/ /
/ /----------------------------------------/ /
/ /             Função decorada            / /
/ / ---------------------------------------/ /
/ /----------------------------------------/ /

"""

# Decorators como funções (Sintaxe não recomendada / Sem Açúcar Sintático)

"""
def seja_educado(funcao):
    def sendo():
        print('Foi um prazer conhecer você!')
        funcao()
        print('Tenha um ótimo dia!')
    return sendo


def saudacao():
    print('Seja bem-vindo(a) a Geek University')
"""

# Testando 1 - Saude, mas seja educado (seja educado é o decorador)
"""

teste = seja_educado(saudacao)

teste()
"""

# Testando 2
"""

def raiva():
    print('EU TE ODEIO!')


raiva_educada = seja_educado(raiva)

raiva_educada()
"""

# Decorators com Syntax Sugar (Açucar Sintática) - Forma recomendada
"""

def seja_educado_mesmo(funcao):
    def sendo():
        print('Foi um prazer conhecer você!')
        funcao()
        print('Tenha um excelente dia!')
    return sendo


@seja_educado_mesmo
def apresentando():
    print('Meu nome é Pedro')

# Testando

apresentando()

"""

# Exemplo de decorator aplicado em um acesso a WebSite

"""
|---------------------------------------------------------------|
| Home    |    Serviços    |   Produtos    |   Administrativo   |
-----------------------------------------------------------------

OBS: Não é código funcional, apenas exemplo de aplicação

def checa_login(): (Decorator fucntion*)
    if not request.usuario:
        redirect('http://www.suaempresa.com.br/login')


def home(request):
    return 'Pode acessar home'

def servicos(request):
    return 'Pode acessar servicos'

def produtos(request):
    return 'Pode acessar produtos'

@checa_login (Decorator*)
def admin(request):
    return 'Pode acessar admin'

"""

# OBS: Não confundir Decorator com Decorator Function









