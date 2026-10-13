#!/usr/bin/env python3
"""
analisador_projeto.py

Analisa um diretório de projeto e produz métricas sobre:
- linguagens identificadas
- arquivos por linguagem
- linhas físicas
- linhas de código (aproximação)
- linhas em branco
- linhas de comentário
- tamanho em bytes
- arquivos por extensão
- maiores arquivos
- diretórios com mais código
- estimativa de complexidade para algumas linguagens
- TODO/FIXME/XXX
- arquivos potencialmente gerados/binários
- arquivos duplicados por hash

Uso:
    python analisador_projeto.py "C:\\MeuProjeto"
    python analisador_projeto.py "/home/user/projeto" --json resultado.json
    python analisador_projeto.py "C:\\MeuProjeto" --top 20

Observação:
As métricas de "código" e "comentário" são heurísticas baseadas em
delimitadores de comentários. Não substituem um parser específico da linguagem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


# extensão -> linguagem
LANGUAGES = {
    ".py": "Python",
    ".pyw": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".c": "C",
    ".h": "C/C++ Header",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++ Header",
    ".hh": "C++ Header",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".phtml": "PHP",
    ".pas": "Delphi/Pascal",
    ".pp": "Delphi/Pascal",
    ".dpr": "Delphi/Pascal",
    ".dpk": "Delphi/Pascal",
    ".dfm": "Delphi Form",
    ".sql": "SQL",
    ".pl": "Perl",
    ".pm": "Perl",
    ".rb": "Ruby",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".dart": "Dart",
    ".r": "R",
    ".R": "R",
    ".lua": "Lua",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".bat": "Batch",
    ".cmd": "Batch",
    ".ps1": "PowerShell",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "Sass",
    ".less": "Less",
#    ".xml": "XML", Não contabilizar arquivos xml nem json
#    ".xsd": "XML Schema",
#    ".json": "JSON", 
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".ini": "INI",
    ".cfg": "Config",
    ".conf": "Config",
    ".md": "Markdown",
    ".tex": "LaTeX",
    ".vue": "Vue",
    ".svelte": "Svelte",
}

# Comentários de linha e bloco.
COMMENT_RULES = {
    "Python": {"line": ["#"], "block": [('"""', '"""'), (", ")]},
    "JavaScript": {"line": ["//"], "block": [("/*", "*/")]},
    "TypeScript": {"line": ["//"], "block": [("/*", "*/")]},
    "Java": {"line": ["//"], "block": [("/*", "*/")]},
    "C": {"line": ["//"], "block": [("/*", "*/")]},
    "C/C++ Header": {"line": ["//"], "block": [("/*", "*/")]},
    "C++": {"line": ["//"], "block": [("/*", "*/")]},
    "C++ Header": {"line": ["//"], "block": [("/*", "*/")]},
    "C#": {"line": ["//"], "block": [("/*", "*/")]},
    "Go": {"line": ["//"], "block": [("/*", "*/")]},
    "Rust": {"line": ["//"], "block": [("/*", "*/")]},
    "PHP": {"line": ["//", "#"], "block": [("/*", "*/")]},
    "Delphi/Pascal": {"line": ["//"], "block": [("{", "}"), ("(*", "*)")]},
    "SQL": {"line": ["--"], "block": [("/*", "*/")]},
    "Perl": {"line": ["#"], "block": []},
    "Ruby": {"line": ["#"], "block": []},
    "Swift": {"line": ["//"], "block": [("/*", "*/")]},
    "Kotlin": {"line": ["//"], "block": [("/*", "*/")]},
    "Dart": {"line": ["//"], "block": [("/*", "*/")]},
    "R": {"line": ["#"], "block": []},
    "Lua": {"line": ["--"], "block": [("--[[", "]]")]},
    "Shell": {"line": ["#"], "block": []},
    "Batch": {"line": ["REM", "::"], "block": []},
    "PowerShell": {"line": ["#"], "block": [("<#", "#>")]},
    "CSS": {"line": [], "block": [("/*", "*/")]},
    "SCSS": {"line": ["//"], "block": [("/*", "*/")]},
    "Sass": {"line": ["//"], "block": []},
    "Less": {"line": ["//"], "block": [("/*", "*/")]},
    "HTML": {"line": [], "block": [("<!--", "-->")]},
    "XML": {"line": [], "block": [("<!--", "-->")]},
    "XML Schema": {"line": [], "block": [("<!--", "-->")]},
    "Vue": {"line": ["//"], "block": [("/*", "*/"), ("<!--", "-->")]},
    "Svelte": {"line": ["//"], "block": [("/*", "*/"), ("<!--", "-->")]},
    "Markdown": {"line": [], "block": [("<!--", "-->")]},
    "LaTeX": {"line": ["%"], "block": []},
    "JSON": {"line": [], "block": []},
    "YAML": {"line": ["#"], "block": []},
    "TOML": {"line": ["#"], "block": []},
    "INI": {"line": [";", "#"], "block": []},
    "Config": {"line": ["#", ";"], "block": []},
}


# Diretórios normalmente irrelevantes para análise de código.
DEFAULT_EXCLUDED_DIRS = {
    ".git", ".svn", ".hg",
    ".venv", "venv", "env", "virtualenv",
    "node_modules",
    "__pycache__",
    ".pytest_cache", ".mypy_cache",
    ".idea", ".vscode",
    "bin", "obj",
    "dist", "build",
    "target",
    "packages",
    "vendor",
}

BINARY_EXTENSIONS = {
    ".exe", ".dll", ".so", ".dylib", ".bin", ".obj", ".o",
    ".a", ".lib", ".class", ".pyc", ".pyd",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico",
    ".zip", ".rar", ".7z", ".gz", ".tar",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".mp3", ".mp4", ".avi", ".mov",
    ".db", ".sqlite", ".sqlite3",
}


@dataclass
class FileMetrics:
    path: str
    language: str
    extension: str
    bytes: int
    lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    todo_count: int
    complexity: int | None = None


def is_probably_binary(path: Path) -> bool:
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return True

    try:
        data = path.read_bytes()[:8192]
    except OSError:
        return True

    return b"\x00" in data


def read_text(path: Path) -> str | None:
    # utf-8 primeiro; depois alguns encodings comuns em projetos antigos.
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except (UnicodeDecodeError, OSError):
            pass
    return None


def classify_lines(text: str, language: str) -> tuple[int, int, int]:
    """
    Retorna (code, comments, blank).
    É uma heurística simples e deliberadamente conservadora.
    """
    rules = COMMENT_RULES.get(language, {"line": [], "block": []})
    line_markers = rules["line"]
    block_markers = rules["block"]

    code = comments = blank = 0
    in_block = None

    for raw in text.splitlines():
        s = raw.strip()

        if not s:
            blank += 1
            continue

        # Dentro de comentário de bloco.
        if in_block:
            comments += 1
            if in_block[1] in s:
                in_block = None
            continue

        # Comentário de bloco iniciando a linha.
        started_block = False
        for start, end in block_markers:
            pos = s.find(start)
            if pos >= 0:
                # Se houver conteúdo de código antes do marcador, conta como código.
                before = s[:pos].strip()
                if before:
                    code += 1
                else:
                    comments += 1

                # Bloco termina na mesma linha?
                if end not in s[pos + len(start):]:
                    in_block = (start, end)

                started_block = True
                break

        if started_block:
            continue

        # Comentário de linha.
        if any(s.startswith(marker) for marker in line_markers):
            comments += 1
        else:
            code += 1

    return code, comments, blank


def estimate_complexity(text: str, language: str) -> int | None:
    """
    Estimativa simples de complexidade ciclomática.
    Não é um parser e pode divergir de ferramentas especializadas.
    """
    supported = {
        "Python", "JavaScript", "TypeScript", "Java", "C", "C++",
        "C#", "Go", "Rust", "PHP", "Delphi/Pascal", "Kotlin",
        "Swift", "Dart", "Ruby"
    }
    if language not in supported:
        return None

    patterns = [
        r"if",
        r"else\s+if",
        r"elif",
        r"for",
        r"while",
        r"case",
        r"catch",
        r"except",
        r"when",
        r"\?\s*[^:]+:",
        r"&&",
        r"\|\|",
        r"and",
        r"or",
    ]

    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, text, flags=re.MULTILINE))

    # Complexidade base = 1 para uma unidade de código.
    return 1 + count


def analyze(root: Path, excluded_dirs: set[str]) -> tuple[list[FileMetrics], Counter, list[str], dict[str, list[str]], list[str]]:
    files: list[FileMetrics] = []
    extension_counts = Counter()
    errors = []
    todos = []
    hash_files: dict[str, list[str]] = defaultdict(list)

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in excluded_dirs for part in path.parts):
            continue

        ext = path.suffix.lower()
        language = LANGUAGES.get(ext)

        # Arquivos sem linguagem conhecida não entram nas métricas de código,
        # mas extensões ainda podem ser reportadas.
        if language is None:
            continue

        if is_probably_binary(path):
            continue

        try:
            size = path.stat().st_size
        except OSError as e:
            errors.append(f"{path}: {e}")
            continue

        text = read_text(path)
        if text is None:
            errors.append(f"{path}: não foi possível decodificar o arquivo")
            continue

        code, comments, blank = classify_lines(text, language)
        physical_lines = len(text.splitlines())
        todo_count = len(re.findall(r"(?:TODO|FIXME|XXX)", text, flags=re.IGNORECASE))
        complexity = estimate_complexity(text, language)

        rel = str(path.relative_to(root))
        files.append(
            FileMetrics(
                path=rel,
                language=language,
                extension=ext,
                bytes=size,
                lines=physical_lines,
                code_lines=code,
                comment_lines=comments,
                blank_lines=blank,
                todo_count=todo_count,
                complexity=complexity,
            )
        )

        extension_counts[ext] += 1

        if todo_count:
            todos.append(f"{rel}: {todo_count}")

        # Hash somente para arquivos pequenos/médios; evita custo desnecessário.
        try:
            if size <= 50 * 1024 * 1024:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                hash_files[digest].append(rel)
        except OSError:
            pass

    return files, extension_counts, errors, hash_files, todos


def human_bytes(n: int) -> str:
    value = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{n} B"


def build_report(root: Path, files: list[FileMetrics], extension_counts: Counter, errors, hash_files, todos, top_n: int):
    by_language = defaultdict(lambda: {
        "files": 0,
        "bytes": 0,
        "lines": 0,
        "code_lines": 0,
        "comment_lines": 0,
        "blank_lines": 0,
        "todo_count": 0,
        "complexity": 0,
    })

    dirs = Counter()

    for f in files:
        d = by_language[f.language]
        d["files"] += 1
        d["bytes"] += f.bytes
        d["lines"] += f.lines
        d["code_lines"] += f.code_lines
        d["comment_lines"] += f.comment_lines
        d["blank_lines"] += f.blank_lines
        d["todo_count"] += f.todo_count
        if f.complexity is not None:
            d["complexity"] += f.complexity

        parent = str(Path(f.path).parent)
        dirs[parent] += f.code_lines

    largest = sorted(files, key=lambda x: x.bytes, reverse=True)[:top_n]
    most_code = sorted(files, key=lambda x: x.code_lines, reverse=True)[:top_n]
    most_complex = sorted(
        [x for x in files if x.complexity is not None],
        key=lambda x: x.complexity,
        reverse=True,
    )[:top_n]

    duplicates = [paths for paths in hash_files.values() if len(paths) > 1]

    report = {
        "project": str(root),
        "files_analyzed": len(files),
        "total_bytes": sum(f.bytes for f in files),
        "total_lines": sum(f.lines for f in files),
        "total_code_lines": sum(f.code_lines for f in files),
        "total_comment_lines": sum(f.comment_lines for f in files),
        "total_blank_lines": sum(f.blank_lines for f in files),
        "total_todos": sum(f.todo_count for f in files),
        "languages": dict(by_language),
        "extensions": dict(extension_counts),
        "directories_by_code_lines": dict(dirs.most_common(top_n)),
        "largest_files": [asdict(x) for x in largest],
        "files_with_most_code": [asdict(x) for x in most_code],
        "files_with_highest_estimated_complexity": [asdict(x) for x in most_complex],
        "duplicate_files": duplicates,
        "todo_files": todos,
        "errors": errors,
        "files": [asdict(x) for x in files],
    }

    return report


def print_report(report, top_n):
    print("=" * 78)
    print("ANÁLISE DO PROJETO")
    print("=" * 78)
    print(f"Projeto:             {report['project']}")
    print(f"Arquivos analisados: {report['files_analyzed']}")
    print(f"Tamanho:             {human_bytes(report['total_bytes'])}")
    print(f"Linhas totais:       {report['total_lines']:,}")
    print(f"Linhas de código:    {report['total_code_lines']:,}")
    print(f"Linhas comentário:   {report['total_comment_lines']:,}")
    print(f"Linhas em branco:    {report['total_blank_lines']:,}")
    print(f"TODO/FIXME/XXX:      {report['total_todos']:,}")

    print("LINGUAGENS")
    print("-" * 78)
    print(f"{'Linguagem':<22} {'Arquivos':>9} {'Código':>12} {'Coment.':>12} {'% código':>10}")
    for lang, d in sorted(
        report["languages"].items(),
        key=lambda item: item[1]["code_lines"],
        reverse=True,
    ):
        pct = 100 * d["code_lines"] / report["total_code_lines"] if report["total_code_lines"] else 0
        print(f"{lang:<22} {d['files']:>9} {d['code_lines']:>12,} {d['comment_lines']:>12,} {pct:>9.1f}%")

    print("EXTENSÕES")
    print("-" * 78)
    for ext, count in sorted(report["extensions"].items(), key=lambda x: x[1], reverse=True):
        print(f"{ext:<12} {count:>8} arquivo(s)")

    print("ARQUIVOS COM MAIS CÓDIGO")
    print("-" * 78)
    for f in report["files_with_most_code"][:top_n]:
        print(f"{f['code_lines']:>8,} linhas | {f['language']:<18} | {f['path']}")

    print("ARQUIVOS MAIORES")
    print("-" * 78)
    for f in report["largest_files"][:top_n]:
        print(f"{human_bytes(f['bytes']):>10} | {f['language']:<18} | {f['path']}")

    print("DIRETÓRIOS COM MAIS CÓDIGO")
    print("-" * 78)
    for directory, lines in report["directories_by_code_lines"].items():
        print(f"{lines:>8,} linhas | {directory}")

    print("MAIOR COMPLEXIDADE ESTIMADA")
    print("-" * 78)
    for f in report["files_with_highest_estimated_complexity"][:top_n]:
        print(f"{f['complexity']:>8} | {f['language']:<18} | {f['path']}")

    if report["duplicate_files"]:
        print("ARQUIVOS DUPLICADOS")
        print("-" * 78)
        for group in report["duplicate_files"][:top_n]:
            print("  " + "  <=>  ".join(group))

    if report["todo_files"]:
        print("TODO / FIXME / XXX")
        print("-" * 78)
        for item in report["todo_files"][:top_n]:
            print(item)

    if report["errors"]:
        print("ARQUIVOS COM ERRO")
        print("-" * 78)
        for error in report["errors"][:top_n]:
            print(error)


def main():
    parser = argparse.ArgumentParser(description="Analisa métricas de um projeto de software.")
    parser.add_argument("directory", nargs="?", help="Diretório raiz do projeto. Se omitido, será solicitado no terminal.")
    parser.add_argument("--json", dest="json_file", help="Salva relatório completo em JSON")
    parser.add_argument("--top", type=int, default=10, help="Quantidade de itens nos rankings (padrão: 10)")
    parser.add_argument(
        "--include",
        nargs="*",
        help="Diretórios adicionais que normalmente seriam ignorados não são alterados; "
             "use esta opção apenas como reserva para extensões futuras.",
    )
    args = parser.parse_args()

    directory = args.directory
    if not directory:
        print("\nAnalisador de Projeto Python")
        print("-" * 40)
        directory = input("Informe o diretório do projeto: ").strip().strip('"')
        if not directory:
            print("Erro: nenhum diretório foi informado.", file=sys.stderr)
            return 2

    root = Path(directory).expanduser().resolve()

    if not root.exists():
        print(f"Erro: diretório não encontrado: {root}", file=sys.stderr)
        return 2

    if not root.is_dir():
        print(f"Erro: não é um diretório: {root}", file=sys.stderr)
        return 2

    files, extensions, errors, hashes, todos = analyze(root, DEFAULT_EXCLUDED_DIRS)
    report = build_report(root, files, extensions, errors, hashes, todos, max(1, args.top))
    print_report(report, max(1, args.top))

    if args.json_file:
        output = Path(args.json_file).expanduser().resolve()
        output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Relatório JSON salvo em: {output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
