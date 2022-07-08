"""
r -> read - Abrea para leitura (padrão)
w -> write - Abre para escrita (sobreescreve caso o arquivo ja exista)
x -> Abre exclusivamente para escrita, falha se o arquivo ja existir
a -> append - Abre para escrita, caso não exista será criado, caso exista será adicionando sempre no final do arquivo
+ -> Abre para o modo de atualizacao, leitura e escrita, tem que ser usado junto com r ou w opção, tem o controle do
     cursor

https://docs.pythin.org/3/library/functions.html#open

"""

# Modo x
"""
try:
    with open('texto2.txt', 'x') as arquivo:
        arquivo.write('Teste com modo de abertura x\n')  # FileExistsError: [Errno 17] File exists: 'texto2.txt'
except FileExistsError:
    print('Arquivo já existe')
"""

# Modo a
"""
with open('texto4.txt', 'a') as arquivo:
    while True:
        fruta = input('informe uma fruta ou digite sair: ')
        if fruta != 'sair':
            arquivo.write(fruta + '\n')
        else:
            break
"""

# Modo

with open('texto4.txt', '+') as arquivo:
    arquivo.seek(0)
    print('Adicionado no inicio')

