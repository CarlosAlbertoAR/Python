import subprocess
import sys
import os

def run_git_command(args, cwd):
    """Executa um comando Git dentro de um diretório específico."""
    try:
        result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar git: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    git_dir = input("Digite o caminho do diretório Git (ex: /caminho/repositorio): ").strip()
    if not git_dir or not os.path.isdir(git_dir):
        print("Diretório inválido.")
        return
    
    search_term = input("Digite a string a ser buscada nos logs do Git: ").strip()
    if not search_term:
        print("Nenhuma string fornecida.")
        return

    # Verifica se é mesmo um repositório Git
    if not os.path.isdir(os.path.join(git_dir, ".git")):
        print("O diretório informado não parece ser um repositório Git válido.")
        return

    # Nome seguro para o arquivo
    safe_filename = search_term.replace(" ", "_") + "-Merge.txt"
    full_output_path = os.path.join(os.getcwd(), safe_filename)

    # Obtém os commits com a string no log
    log_output = run_git_command(["log", "--grep", search_term, "--pretty=format:%H"], cwd=git_dir)
    commit_hashes = log_output.splitlines()

    if not commit_hashes:
        print("Nenhum commit encontrado com essa string.")
        return

    status_groups = {
        "A": set(),
        "M": set(),
        "D": set(),
        "R": set(),
    }

    for commit in commit_hashes:
        diff_output = run_git_command(["show", "--pretty=", "--name-status", commit], cwd=git_dir)
        for line in diff_output.splitlines():
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                status_code = parts[0]
                if status_code.startswith("R"):
                    path = parts[-1]
                    status_groups["R"].add(path)
                elif status_code in status_groups:
                    path = parts[1]
                    status_groups[status_code].add(path)

    status_labels = {
        "A": "Adicionados",
        "M": "Modificados",
        "D": "Deletados",
        "R": "Renomeados"
    }

    output_lines = [f"Arquivos afetados por commits contendo '{search_term}':\n"]

    for code in ["A", "M", "D", "R"]:
        files = sorted(status_groups[code])
        if files:
            output_lines.append(f"{status_labels[code]}:")
            for f in files:
                output_lines.append(f"  {f}")
            output_lines.append("")

    output_text = "\n".join(output_lines)

    with open(full_output_path, "w", encoding="utf-8") as f:
        f.write(output_text)

    print("\n" + output_text)
    print(f"Resultado salvo em: {full_output_path}")

if __name__ == "__main__":
    main()
