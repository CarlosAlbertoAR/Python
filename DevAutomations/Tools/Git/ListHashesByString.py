#!/usr/bin/env python3
"""
Script para buscar, em um repositório Git, commits cuja mensagem de log
contenha um determinado texto, e gerar um arquivo .txt com os hashes
encontrados, ordenados do mais recente para o mais antigo.
"""

import os
import subprocess
import sys
from datetime import datetime


def ask_git_directory():
    while True:
        caminho = input("Informe o caminho do diretório do repositório Git: ").strip()
        caminho = os.path.abspath(os.path.expanduser(caminho))

        if not os.path.isdir(caminho):
            print(f'Erro: o diretório "{caminho}" não existe.\n')
            continue

        if not os.path.isdir(os.path.join(caminho, ".git")):
            print(f'Erro: "{caminho}" não parece ser um repositório Git (pasta .git não encontrada).\n')
            continue

        return caminho


def ask_search_text():
    while True:
        texto = input("Informe o texto a ser procurado nas mensagens de commit: ").strip()
        if texto:
            return texto
        print("O texto não pode ser vazio.\n")


def search_commits(diretorio, texto):
    """
    Usa `git log --grep` para localizar commits cuja mensagem contenha o texto.
    --date-order garante que os commits venham do mais recente para o mais antigo.
    --no-merges exclui commits de merge da busca (não interessam para cherry-pick).
    -i torna a busca case-insensitive (remova o -i se quiser case-sensitive).
    """
    comando = [
        "git",
        "-C", diretorio,
        "log",
        "--date-order",
        "--no-merges",
        "-i",
        f"--grep={texto}",
        "--pretty=format:%H|%ad|%s",
        "--date=short",
    ]

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if resultado.returncode != 0:
        print("Erro ao executar o git log:")
        print(resultado.stderr)
        sys.exit(1)

    saida = resultado.stdout.strip()
    if not saida:
        return []

    commits = []
    for linha in saida.split("\n"):
        partes = linha.split("|", 2)
        if len(partes) == 3:
            hash_commit, data, mensagem = partes
            commits.append((hash_commit, data, mensagem))

    return commits


def generate_txt_file(commits, texto_busca, diretorio):
    nome_repo = texto_busca
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"hashes_{nome_repo}_{timestamp}.txt"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"Repositório: {diretorio}\n")
        f.write(f"Texto pesquisado: {texto_busca}\n")
        f.write(f"Total de commits encontrados: {len(commits)}\n")
        f.write("Ordenação: do mais recente para o mais antigo\n")
        f.write("-" * 60 + "\n\n")

        for hash_commit, data, mensagem in commits:
            f.write(f"{hash_commit}\n")

        f.write("\n" + "-" * 60 + "\n")
        f.write("Detalhamento (hash | data | mensagem):\n\n")
        for hash_commit, data, mensagem in commits:
            f.write(f"{hash_commit} | {data} | {mensagem}\n")

        # O cherry-pick deve ser aplicado do commit mais antigo para o mais novo,
        # para preservar a ordem cronológica original das alterações.
        # Como a lista acima está do mais recente para o mais antigo, invertemos aqui.
        hashes_ordem_cronologica = [hash_commit for hash_commit, _, _ in reversed(commits)]
        comando_cherry_pick = "git cherry-pick " + " ".join(hashes_ordem_cronologica)

        f.write("\n" + "-" * 60 + "\n")
        f.write("Comando para aplicar os commits via cherry-pick\n")
        f.write("(ordem cronológica: do mais antigo para o mais novo):\n\n")
        f.write(comando_cherry_pick + "\n")

    return nome_arquivo


def main():
    print("=== Busca de commits Git por texto na mensagem de log ===\n")

    diretorio = ask_git_directory()
    texto = ask_search_text()

    print(f'\nBuscando commits contendo "{texto}" em "{diretorio}"...\n')

    commits = search_commits(diretorio, texto)

    if not commits:
        print("Nenhum commit encontrado com o texto informado.")
        return

    arquivo_gerado = generate_txt_file(commits, texto, diretorio)

    print(f"{len(commits)} commit(s) encontrado(s).")
    print(f"Arquivo gerado: {os.path.abspath(arquivo_gerado)}")


if __name__ == "__main__":
    main()