import os
import zipfile
import py7zr
import logging

from database_sqlserver import SQLServerDatabase
from database_postgres import PostgresDatabase
from database_sqlanywhere import SQLAnywhereDatabase

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Assinaturas binárias (magic bytes) usadas para reconhecer contêineres
# compactados mesmo quando o arquivo chega sem extensão.
ZIP_MAGIC = b'PK\x03\x04'
SEVEN_Z_MAGIC = b'7z\xbc\xaf\x27\x1c'
RAR_MAGIC = b'Rar!\x1a\x07'


class UnsupportedBackupTypeException(Exception):
    """Levantada quando o tipo de backup não pôde ser identificado como SQL Server, PostgreSQL, Sybase/SQL Anywhere ou script SQL em texto."""
    pass


def _read_header(file_path, size=8192):
    with open(file_path, 'rb') as f:
        return f.read(size)


def extract_file(file_path, destination_folder):
    """
    Descompacta arquivos .zip, .7z ou .rar (reconhecidos por extensão OU
    por assinatura binária, já que o arquivo pode chegar sem extensão,
    inclusive vindo de um caminho de rede "\\\\servidor\\pasta\\arquivo")
    para destination_folder, e retorna o caminho do arquivo de backup
    encontrado dentro dela.

    Se o arquivo informado já estiver descompactado (não for reconhecido
    como um contêiner compactado), retorna o próprio caminho de origem sem
    copiá-lo em nenhum momento -- cobrindo o caso de um backup já
    descompactado disponível diretamente em um compartilhamento de rede,
    que é restaurado direto da origem.
    """
    filename = os.path.basename(file_path)
    lower_name = filename.lower()
    header = _read_header(file_path)

    is_zip = lower_name.endswith('.zip') or header.startswith(ZIP_MAGIC)
    is_7z = lower_name.endswith('.7z') or header.startswith(SEVEN_Z_MAGIC)
    is_rar = lower_name.endswith('.rar') or header.startswith(RAR_MAGIC)

    if not (is_zip or is_7z or is_rar):
        # Não é um contêiner compactado reconhecido: já está "descompactado"
        # -- restaura direto da origem (local ou de rede), sem copiar.
        return file_path

    os.makedirs(destination_folder, exist_ok=True)

    if is_zip:
        logging.info(f"Extraindo ZIP: {filename}")
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)

    elif is_7z:
        logging.info(f"Extraindo 7z: {filename}")
        with py7zr.SevenZipFile(file_path, mode='r') as z:
            z.extractall(path=destination_folder)

    elif is_rar:
        logging.info(f"Extraindo RAR: {filename}")
        try:
            import rarfile
            rarfile.SEVENZIP_TOOL = r"C:\Program Files\7-Zip\7z.exe" #Encontrar melhor ajuste, colocar no path, etc
        except ImportError as exc:
            raise ImportError(
                "Suporte a .rar requer o pacote 'rarfile' (pip install rarfile) "
                "e o utilitário 'unrar' (ou 'bsdtar'/'7z') disponível no PATH."
            ) from exc
        with rarfile.RarFile(file_path, 'r') as rf:
            rf.extractall(path=destination_folder)

    # Reúne todos os arquivos extraídos para localizar o backup entre eles.
    candidates = []
    for root, _dirs, files in os.walk(destination_folder):
        for extracted_file in files:
            candidates.append(os.path.join(root, extracted_file))

    if not candidates:
        return None

    # Prioriza extensões conhecidas de backup/dump/script.
    preferred_ext = ('.bak', '.dump', '.sql', '.db', '.backup')
    preferred = [c for c in candidates if c.lower().endswith(preferred_ext)]
    if preferred:
        return preferred[0]

    # Nenhuma extensão reconhecida: assume o maior arquivo extraído como
    # sendo o backup (arquivos auxiliares tendem a ser bem menores).
    return max(candidates, key=os.path.getsize)


def detect_backup_type(file_path):
    """
    Identifica o SGBD de origem de um arquivo de backup pelo conteúdo
    (assinatura binária / heurística de texto), já que o arquivo pode não
    ter extensão.

    Retorna uma das strings: 'sqlserver', 'postgres', 'sybase', 'sql_text'.
    Levanta UnsupportedBackupTypeException se nenhum tipo for reconhecido.

    IMPORTANTE: apenas a assinatura do PostgreSQL (formato "custom" do
    pg_dump, "PGDMP") é oficialmente documentada e, portanto, confiável.
    A detecção de backups nativos do SQL Server (.bak, Microsoft Tape
    Format) e do Sybase/SQL Anywhere é heurística, já que esses são
    formatos proprietários sem especificação binária pública completa.
    Em caso de falso negativo, renomeie o arquivo com a extensão correta
    ou ajuste as heurísticas abaixo para o seu ambiente.
    """
    header = _read_header(file_path)

    # PostgreSQL: formato "custom" do pg_dump (-Fc) começa com a
    # assinatura oficial "PGDMP".
    if header[:5] == b'PGDMP':
        return 'postgres'

    # SQL Server: backups nativos (.bak) usam o Microsoft Tape Format
    # (MTF), cujo bloco de cabeçalho de mídia começa com a assinatura
    # ASCII "TAPE".
    if header[:4] == b'TAPE':
        return 'sqlserver'

    # Sybase / SQL Anywhere: sem assinatura binária pública documentada;
    # heurística baseada no nome do produto aparecendo no cabeçalho do
    # arquivo (vale tanto para o .db quanto para backups gerados via
    # BACKUP DATABASE, que são cópias do próprio arquivo .db).
    if b'SQL Anywhere' in header or b'Adaptive Server Anywhere' in header or b'Sybase' in header:
        return 'sybase'

    # Nenhuma assinatura binária reconhecida: tenta interpretar como
    # script SQL em texto puro.
    try:
        sample_upper = header.decode('utf-8').upper()
        sql_keywords = ('CREATE TABLE', 'CREATE DATABASE', 'INSERT INTO', 'BEGIN TRANSACTION', 'SELECT ', '--')
        if any(kw in sample_upper for kw in sql_keywords):
            return 'sql_text'
    except UnicodeDecodeError:
        pass

    raise UnsupportedBackupTypeException(
        f"Não foi possível identificar o tipo de backup do arquivo '{file_path}'. "
        "Formatos suportados: SQL Server (.bak), PostgreSQL (dump custom), "
        "Sybase/SQL Anywhere, ou script SQL em texto puro."
    )


def restore_sql_server_backup(
    bak_path, db_name, server='localhost',
    user=None, password=None, driver="ODBC Driver 17 for SQL Server",
) -> bool:
    """
    Restaura um backup nativo do SQL Server (.bak) usando a classe
    SQLServerDatabase (sqlserver_database.py). O RESTORE DATABASE do SQL
    Server já cria o banco como parte do próprio processo, então nenhuma
    etapa de criação prévia é necessária aqui.
    """
    db = SQLServerDatabase(
        server=server,
        database=db_name,
        user=user,
        password=password,
        driver=driver,
        trusted_connection=user is None,
    )
    logging.info(f"Iniciando restauração da base [{db_name}] no SQL Server...")
    if db.restore(bak_path):
        logging.info("Restauração concluída com sucesso!")
        return True
    logging.error(f"Erro ao restaurar banco de dados: {db.get_last_error()}")
    return False


def restore_postgres_backup(
    dump_path, db_name, server='localhost',
    port=5432, user='postgres', password='',
) -> bool:
    """
    Restaura um dump do PostgreSQL (formato custom do pg_dump, -Fc) usando
    a classe PostgresDatabase (postgres_database.py). Diferente do SQL
    Server, o pg_restore exige que o banco de destino já exista -- por
    isso ele é criado aqui automaticamente caso ainda não exista.
    """
    db = PostgresDatabase(host=server, port=port, user=user, password=password, dbname=db_name)

    if not db.exists(db_name):
        logging.info(f"Base [{db_name}] não existe; criando...")
        if not db.create(db_name):
            logging.error(f"Erro ao criar banco de dados: {db.get_last_error()}")
            return False

    logging.info(f"Iniciando restauração da base [{db_name}] no PostgreSQL...")
    if db.restore(dump_path):
        logging.info("Restauração concluída com sucesso!")
        return True
    logging.error(f"Erro ao restaurar banco de dados: {db.get_last_error()}")
    return False


def restore_sql_anywhere_backup(
    bak_path, db_name, server='localhost',
    host=None, port=2638, user='dba', password='sql',
) -> bool:
    """
    "Restaura" um backup do Sybase/SQL Anywhere usando a classe
    SQLAnywhereDatabase (sqlanywhere_database.py). O SQL Anywhere não tem
    um comando SQL "RESTORE DATABASE" (ver ressalvas no próprio módulo);
    o backup gerado via BACKUP DATABASE é uma cópia consistente do
    arquivo .db, então "restaurar" é iniciar o engine diretamente contra
    esse arquivo, o que é feito internamente por SQLAnywhereDatabase.restore().
    """
    db = SQLAnywhereDatabase(
        server=server, database=db_name, user=user, password=password,
        host=host or server, port=port,
    )
    logging.info(f"Iniciando restauração da base [{db_name}] no SQL Anywhere...")
    if db.restore(bak_path):
        logging.info("Restauração concluída com sucesso!")
        return True
    logging.error(f"Erro ao restaurar banco de dados: {db.get_last_error()}")
    return False


def main():
    # Aceita tanto caminhos locais quanto caminhos de rede
    # ("\\\\servidor\\pasta\\arquivo").
    file_input = input(
        "Digite o caminho completo do arquivo (local ou de rede; "
        ".zip, .7z, .rar, .bak, .sql, etc.): "
    ).strip('"')

    if not os.path.exists(file_input):
        print("Arquivo não encontrado!")
        return

    destination_folder = input(
        "Digite a pasta de destino para extração (e para a base já "
        "descompactada, quando aplicável): "
    ).strip('"')

    delete_extracted_input = input(
        "Excluir o backup extraído após a restauração (não afeta o "
        "arquivo de origem)? (s/N): "
    ).strip().lower()
    delete_extracted_backup = delete_extracted_input == 's'

    try:
        backup_file = extract_file(file_input, destination_folder)
    except Exception as exc:
        logging.error(f"Erro ao extrair o arquivo: {exc}")
        return

    if not backup_file:
        print("Não foi possível localizar um arquivo de backup válido no caminho fornecido.")
        return

    print(f"Arquivo de backup identificado: {backup_file}")

    try:
        backup_type = detect_backup_type(backup_file)
    except UnsupportedBackupTypeException as exc:
        logging.error(str(exc))
        return

    print(f"Tipo de backup detectado: {backup_type}")

    db_target = input("Digite o nome da base de dados para a restauração: ")
    sql_server = input("Servidor (Padrão: localhost): ") or "localhost"
    user = input("Usuário (deixe em branco para autenticação integrada, quando suportado): ").strip() or None
    password = input("Senha: ") if user else None

    success = False
    try:
        if backup_type == 'sqlserver':
            success = restore_sql_server_backup(backup_file, db_target, server=sql_server, user=user, password=password)

        elif backup_type == 'postgres':
            success = restore_postgres_backup(
                backup_file, db_target, server=sql_server,
                user=user or 'postgres', password=password or '',
            )

        elif backup_type == 'sybase':
            success = restore_sql_anywhere_backup(
                backup_file, db_target, server=sql_server,
                user=user or 'dba', password=password or 'sql',
            )

        elif backup_type == 'sql_text':
            print(
                "Arquivo identificado como script SQL em texto puro. A execução "
                "direta desse tipo de arquivo não está implementada neste script "
                "-- utilize a ferramenta de linha de comando do SGBD de destino "
                "(sqlcmd, psql ou dbisql)."
            )
    finally:
        # Exclui apenas o backup que foi extraído, nunca o arquivo de
        # origem informado pelo usuário -- e somente se a restauração
        # tiver sido concluída com sucesso.
        was_extracted = backup_file != file_input
        if delete_extracted_backup and was_extracted and success and os.path.exists(backup_file):
            try:
                os.remove(backup_file)
                logging.info(f"Backup extraído removido: {backup_file}")
            except Exception as exc:
                logging.warning(f"Não foi possível remover o backup extraído: {exc}")


if __name__ == "__main__":
    main()
