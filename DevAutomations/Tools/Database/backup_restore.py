"""
backup_restore_ticket.py

Refatoração orientada a objetos do script de restauração de backup.

Classes:
    DatabaseServer    -- agrupa os parâmetros de conexão (server, database,
                          user, password, driver, trusted_connection, e os
                          extras opcionais host/port) usados para construir
                          a instância de Database correta depois que o tipo
                          de backup é identificado.

    BackupRestoreticket   -- representa um "ticket" de restauração: liga um
                          arquivo de origem (file_input) a uma base de
                          destino (database_name) em um servidor (server),
                          orquestrando extração, detecção de tipo,
                          restauração (via SQLServerDatabase /
                          PostgresDatabase / SQLAnywhereDatabase) e,
                          opcionalmente, execução de scripts SQL
                          pós-restauração.

As funções utilitárias extract_file() e detect_backup_type(), e a exceção
UnsupportedBackupTypeException, continuam como funções de módulo (não
dependem de estado de instância) e são reaproveitadas internamente pelo ticket.
"""

import os
import uuid
import zipfile
import py7zr
import logging
from datetime import datetime

from database_sqlserver import SQLServerDatabase
from database_postgres import PostgresDatabase
from database_sqlanywhere import SQLAnywhereDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Assinaturas binárias (magic bytes) usadas para reconhecer contêineres
# compactados mesmo quando o arquivo chega sem extensão.
ZIP_MAGIC = b'PK\x03\x04'
SEVEN_Z_MAGIC = b'7z\xbc\xaf\x27\x1c'
RAR_MAGIC = b'Rar!\x1a\x07'


class UnsupportedBackupTypeException(Exception):
    """Levantada quando o tipo de backup não pôde ser identificado como
    SQL Server, PostgreSQL, Sybase/SQL Anywhere ou script SQL em texto,
    ou quando não há classe Database associada ao tipo identificado."""
    pass


# ---------------------------------------------------------------------------
# Funções utilitárias (sem estado, reaproveitadas pelo ticket)
# ---------------------------------------------------------------------------
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
            # Ajuste o caminho do executável do 7-Zip conforme o seu
            # ambiente (necessário caso o 'unrar' não esteja no PATH).
            rarfile.SEVENZIP_TOOL = r"C:\Program Files\7-Zip\7z.exe"
        except ImportError as exc:
            raise ImportError(
                "Suporte a .rar requer o pacote 'rarfile' (pip install rarfile) "
                "e o utilitário 'unrar' (ou 'bsdtar'/'7z') disponível no PATH."
            ) from exc
        with rarfile.RarFile(file_path, 'r') as rf:
            rf.extractall(path=destination_folder)

    candidates = []
    for root, _dirs, files in os.walk(destination_folder):
        for extracted_file in files:
            candidates.append(os.path.join(root, extracted_file))

    if not candidates:
        return None

    preferred_ext = ('.bak', '.dump', '.sql', '.db', '.backup')
    preferred = [c for c in candidates if c.lower().endswith(preferred_ext)]
    if preferred:
        return preferred[0]

    return max(candidates, key=os.path.getsize)


def detect_backup_type(file_path):
    """
    Identifica o SGBD de origem de um arquivo de backup pelo conteúdo.
    Retorna 'sqlserver', 'postgres', 'sybase' ou 'sql_text'.
    Levanta UnsupportedBackupTypeException se nenhum tipo for reconhecido.

    IMPORTANTE: apenas a assinatura do PostgreSQL ("PGDMP") é oficialmente
    documentada. A detecção de SQL Server e Sybase/SQL Anywhere é
    heurística -- ver observações no README / docstring original.
    """
    header = _read_header(file_path)

    if header[:5] == b'PGDMP':
        return 'postgres'

    if header[:4] == b'TAPE':
        return 'sqlserver'

    if b'SQL Anywhere' in header or b'Adaptive Server Anywhere' in header or b'Sybase' in header:
        return 'sybase'

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


# ---------------------------------------------------------------------------
# ConnectionSettings -- parâmetros de conexão
# ---------------------------------------------------------------------------
class ConnectionSettings:
    """
    Agrupa os parâmetros de conexão usados para instanciar a classe
    Database correta (SQLServerDatabase, PostgresDatabase ou
    SQLAnywhereDatabase) depois que o tipo de backup é identificado.

    Propriedades pedidas: server, database, user, password, driver,
    trusted_connection. Também aceita `host` e `port` opcionais, já que
    Postgres e SQL Anywhere distinguem endereço de rede (host/porta) de
    nome lógico do servidor -- quando não informado, `host` usa o mesmo
    valor de `server`.
    """

    def __init__(
        self,
        server,
        database=None,
        user=None,
        password=None,
        driver=None,
        trusted_connection=False,
        host=None,
        port=None,
    ):
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.driver = driver
        self.trusted_connection = trusted_connection
        self.host = host or server
        self.port = port

    def __repr__(self):
        return (
            f"DatabaseServer(server={self.server!r}, database={self.database!r}, "
            f"user={self.user!r}, driver={self.driver!r}, "
            f"trusted_connection={self.trusted_connection})"
        )


# ---------------------------------------------------------------------------
# BackupRestoreticket
# ---------------------------------------------------------------------------
class BackupRestore:
    """
    Representa uma restauração de backup: identificador (ticket_id) +
    arquivo de origem + base de destino + servidor + (opcionalmente)
    scripts SQL a executar após a restauração.

    Uso básico:
        connection = ConnectionSettings(server="localhost", user="sa", password="...")
        restore = BackupRestore(
            file_input=r"\\\\fileserver\\backups\\base.zip",
            destination_folder=r"C:\\restores",
            database_name="MinhaBase",
            connection=connection,
            delete_extracted_backup=True,
            post_restore_scripts=["scripts/pos_restore.sql"],
        )
        ok = restore.run()
        print(restore.to_dict())
    """

    def __init__(
        self,
        file_input,
        destination_folder,
        database_name,
        connection_settings: ConnectionSettings,
        ticket_id=None,
        delete_extracted_backup=False,
        post_restore_scripts=None,
        backup_type_override=None,
        dry_run=False,
        on_success=None,
        on_failure=None,
    ):
        self.ticket_id = ticket_id or f"ticket_{uuid.uuid4().hex[:8]}"

        # Inicializa os atributos "privados" usados pelas properties antes
        # de atribuir via setter (file_input não depende dos demais;
        self._destination_folder = None
        self._database_name = None

        self.file_input = file_input
        self.destination_folder = destination_folder
        self.database_name = database_name
        self.connection_settings = connection_settings

        self.delete_extracted_backup = delete_extracted_backup
        self.post_restore_scripts = post_restore_scripts or []
        self.backup_type_override = backup_type_override
        self.dry_run = dry_run
        self.on_success = on_success
        self.on_failure = on_failure

        # Estado de execução (preenchido por run())
        self.status = "pending"
        self.backup_file = None
        self.backup_type = None
        self.success = False
        self.error_message = None
        self.started_at = None
        self.finished_at = None
        self.log_entries = []

    # --- properties com validação -----------------------------------
    @property
    def file_input(self):
        return self._file_input

    @file_input.setter
    def file_input(self, value):
        if isinstance(value, str):
            value = value.strip('"').strip()
        if not value or not os.path.exists(value):
            raise FileNotFoundError(f"Arquivo de origem não encontrado: {value}")
        self._file_input = value

    @property
    def destination_folder(self):
        return self._destination_folder

    @destination_folder.setter
    def destination_folder(self, value):
        if isinstance(value, str):
            value = value.strip('"').strip()
        self._destination_folder = value

    @property
    def database_name(self):
        return self._database_name

    @database_name.setter
    def database_name(self, value):
        if isinstance(value, str):
            value = value.strip()
        if not value:
            raise ValueError("database_name não pode ser vazio.")
        self._database_name = value

    @property
    def connection_settings(self):
        return self._connection_settings

    @connection_settings.setter
    def connection_settings(self, value):
        if not isinstance(value, ConnectionSettings):
            raise TypeError("connection_settings deve ser uma instância de ConnectionSettings.")
        self._connection_settings= value

    # --- log / auditoria ----------------------------------------------
    def _log(self, message, level="info"):
        timestamp = datetime.now().isoformat(timespec="seconds")
        self.log_entries.append(f"[{timestamp}] {message}")
        log_fn = getattr(logging, level, logging.info)
        log_fn(f"[{self.ticket_id}] {message}")

    # --- construção da instância de Database correta -------------------
    def _build_database_instance(self):
        if self.backup_type == 'sqlserver':
            return SQLServerDatabase(
                server=self.connection_settings.server,
                port=self.connection_settings.port or 1433,
                database=self.database_name,
                user=self.connection_settings.user,
                password=self.connection_settings.password,
                driver=self.connection_settings.driver or "ODBC Driver 17 for SQL Server",
                trusted_connection=self.connection_settings.trusted_connection,
            )
        if self.backup_type == 'postgres':
            return PostgresDatabase(
                host=self.connection_settings.host,
                port=self.connection_settings.port or 5432,
                user=self.connection_settings.user or 'postgres',
                password=self.connection_settings.password or '',
                dbname=self.database_name,
            )
        if self.backup_type == 'sybase':
            return SQLAnywhereDatabase(
                server=self.connection_settings.server,
                database=self.database_name,
                user=self.connection_settings.user or 'dba',
                password=self.connection_settings.password or 'sql',
                driver=self.connection_settings.driver or "SQL Anywhere 17",
                host=self.connection_settings.host,
            )
        raise UnsupportedBackupTypeException(
            f"Não há classe Database associada ao tipo de backup '{self.backup_type}'."
        )

    def _restore(self, db):
        if self.backup_type == 'postgres':
            if not db.exists(self.database_name):
                self._log(f"Base '{self.database_name}' não existe no PostgreSQL; criando...")
                if not db.create(self.database_name):
                    return False
            return db.restore(self.backup_file)
        
        # SQL Server e SQL Anywhere já tratam criação/abertura do banco
        # dentro do próprio restore() (ver database_sqlserver.py /
        # database_sqlanywhere.py).
        return db.restore(self.backup_file)

    def _resolve_script(self, script):
        """Aceita tanto um caminho para arquivo .sql quanto SQL puro em string."""
        if isinstance(script, str) and os.path.isfile(script):
            with open(script, 'r', encoding='utf-8') as f:
                return f.read()
        return script

    def _run_post_restore_scripts(self, db):
        """
        Executa, em sequência, os scripts SQL de post_restore_scripts
        contra a base recém-restaurada, usando a mesma instância de
        Database (SQLServerDatabase / PostgresDatabase /
        SQLAnywhereDatabase) já resolvida para este ticket.
        """
        all_ok = True
        if not db.is_connected():
            if not db.connect():
                self._log(f"Erro ao conectar para scripts pós-restore: {db.get_last_error()}", level="error")
                return False

        total = len(self.post_restore_scripts)
        for i, script in enumerate(self.post_restore_scripts, start=1):
            sql_text = self._resolve_script(script)
            self._log(f"Executando script pós-restore {i}/{total}...")
            if not db.execute_sql(sql_text):
                self._log(f"Erro no script pós-restore {i}: {db.get_last_error()}", level="error")
                all_ok = False
        return all_ok

    def _cleanup_extracted_backup(self):
        """Remove apenas o backup extraído (nunca o file_input de origem),
        e somente se a restauração tiver sido concluída com sucesso."""
        was_extracted = self.backup_file is not None and self.backup_file != self.file_input
        if self.delete_extracted_backup and was_extracted and self.success and os.path.exists(self.backup_file):
            try:
                os.remove(self.backup_file)
                self._log(f"Backup extraído removido: {self.backup_file}")
            except Exception as exc:
                self._log(f"Não foi possível remover o backup extraído: {exc}", level="warning")

    # --- orquestração principal -----------------------------------------
    def run(self) -> bool:
        """
        Executa o restore por completo: extrai (se necessário), identifica o
        tipo de backup, restaura usando a classe Database correspondente,
        roda os scripts pós-restore (se houver) e faz a limpeza do backup
        extraído (se configurado). Atualiza self.status/self.success e
        retorna True/False.
        """
        self.status = "running"
        self.started_at = datetime.now()
        self._log(f"Restore iniciado: '{self.file_input}' -> base '{self.database_name}' em '{self.connection_settings.server}'.")

        try:
            self.backup_file = extract_file(self.file_input, self.destination_folder)
            if not self.backup_file:
                raise RuntimeError("Não foi possível localizar um arquivo de backup válido no caminho fornecido.")
            self._log(f"Arquivo de backup identificado: {self.backup_file}")

            self.backup_type = self.backup_type_override or detect_backup_type(self.backup_file)
            origem = "forçado manualmente" if self.backup_type_override else "detectado automaticamente"
            self._log(f"Tipo de backup: {self.backup_type} ({origem}).")

            if self.backup_type == 'sql_text' and not self.backup_type_override:
                self._log(
                    "Script SQL em texto puro detectado; informe "
                    "backup_type_override ('sqlserver'/'postgres'/'sybase') ao "
                    "criar o restore para executá-lo automaticamente, ou rode-o "
                    "manualmente com a ferramenta de linha de comando do SGBD.",
                    level="warning",
                )
                self.status = "skipped"
                return False

            if self.dry_run:
                self._log("dry_run=True: nenhuma restauração será executada.")
                self.status = "dry_run"
                return True

            db = self._build_database_instance()

            if self.backup_type == 'sql_text':
                # backup_type_override indicou o engine: executa o script
                # diretamente em vez de chamar restore().
                if not db.connect():
                    raise RuntimeError(f"Erro ao conectar: {db.get_last_error()}")
                if not db.execute_sql(self._resolve_script(self.backup_file)):
                    raise RuntimeError(f"Erro ao executar script: {db.get_last_error()}")
            else:
                if not self._restore(db):
                    raise RuntimeError(f"Falha na restauração: {db.get_last_error()}")

            self._log("Restauração concluída com sucesso.")

            if self.post_restore_scripts:
                if not self._run_post_restore_scripts(db):
                    self._log("Um ou mais scripts pós-restore falharam.", level="warning")

            self.success = True
            self.status = "success"
            if self.on_success:
                self.on_success(self)
            return True

        except Exception as exc:
            self.success = False
            self.status = "failed"
            self.error_message = str(exc)
            self._log(f"Erro no restore: {exc}", level="error")
            if self.on_failure:
                self.on_failure(self, exc)
            return False

        finally:
            self.finished_at = datetime.now()
            self._cleanup_extracted_backup()

    # --- utilidades -------------------------------------------------
    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "file_input": self.file_input,
            "destination_folder": self.destination_folder,
            "database_name": self.database_name,
            "server": self.connection_settings.server,
            "status": self.status,
            "backup_type": self.backup_type,
            "backup_file": self.backup_file,
            "success": self.success,
            "error_message": self.error_message,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
        }

    def __repr__(self):
        return f"<BackupRestoreticket {self.ticket_id} status={self.status!r} database_name={self.database_name!r}>"
