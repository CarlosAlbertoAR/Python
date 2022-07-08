"""
Sorted

- Como o próprio nome diz, sorted()server para ordenar.

- OBS: Não confunda apesar no nome, com  função sort() que estudamosem Listas. o sort() só funciona em listas.

- Podemos utilizar o sorted() com qualquer iterável.

- Retorna sempre uma lista com os elementos do iterável ordenados independente se está sendo utilizado em set ou tupla

- Retorna uma lista gerada , nao ordena a passada como parâmetro

"""

# Exemplo
"""
numeros = [6, 1, 8, 2]
print(numeros)

print(sorted(numeros))  # Ordenar do menor para o maior

print(numeros)
"""

# Adicionando parâmetros ao sorted()
"""
numeros = [6, 1, 8, 2]

print(sorted(numeros, reverse=True))  # Ordena em ordem descrecente
"""

# Podemos utilizar o sorted() para coisas mais complexas
"""
usuarios = [
    {"username": "samuel", "tweets": ["Eu adoro bolos", "Eu Adoro pizzas"]},
    {"username": "carla", "tweets": ["Eu amo meus gato"]},
    {"username": "jeff", "tweets": []},
    {"username": "bob", "tweets": []},
    {"username": "doggo", "tweets": ["Eu gosto de cachorros", "Vou sair hoje"]},
    {"username": "gal", "tweets": []}
]

print(usuarios)

# print(sorted(usuarios))  # Erro se não passado a chave no caso de um dicionário

print(sorted(usuarios, key=lambda usuario: usuario["username"]))  # Podendo inclusive passar uma função como valor da chave


# Ordenando pelo número de tweets
print(sorted(usuarios, key=lambda usuario: len(usuario["tweets"])))
"""

# Último exemplo

musicas = [
    {"titulo": "Thunderstruck", "tocou": 3},
    {"titulo": "Dead Skin Mask", "tocou": 2},
    {"titulo": "Back in Black", "tocou": 4},
    {"titulo": "Too old to rock'in'roll", "tocou": 32}
]

# Ordena da menos tocada para mais tocada
print(sorted(musicas, key=lambda musica: musica['tocou']))

# Ordena da mais tocada para menos tocada
print(sorted(musicas, key=lambda musica: musica['tocou'], reverse=True))

