"""
Escrevendo em arquivos

OBS: Ao abrir um arquivo para leitura, não podemos realizar a escrita, apenas ler.
Da mesma forma, se abrirmos o arquivo para escrita, não podemos lê-lo, somente escrever nele.

Ao abrir um arquivo para escrita, o arquivo é criado no armazenamento de disco.

Para escrever dados no arquivo, após aberto, utilizamos a função write().

Abrindo um arquivo para escrita com o modo 'w' se não existir, sera criado.
Caso ele já exista, o anterior será sobrescrito. Dessa forma seu conteúdo será perdido.

"""

# Exemplo de escrita - modo 'W' - write (escrita)

with open('texto2.txt', 'w') as arquivo:
    arquivo.write('É muito facil escreve com write() em Python.\n')
    arquivo.write('Podemos colocar quantas linhas quisermos.\n')
    arquivo.write('Esta é a última linha.')

# Escrevendo muitas strings com um só comando

with open('texto3.txt', 'w') as arquivo:
    arquivo.write('geek' * 1000)

with open('texto4.txt', 'w') as arquivo:
    while True:
        fruta = input('informe uma fruta ou digite sair: ')
        if fruta != 'sair':
            arquivo.write(fruta + '\n')
        else:
            break



