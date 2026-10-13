"""
sqlanywhere_database.py

Sybase / SAP SQL Anywhere implementation of the interfaces defined in
database.py (Database, Index, Check, Column, Table), using pyodbc.

Requirements:
    pip install pyodbc
    A SQL Anywhere ODBC driver installed on the host machine
    (e.g. "SQL Anywhere 17", "SQL Anywhere 12", or the generic "SQLAnywhere"
    driver name registered by the SQL Anywhere / SAP SQL Anywhere client).

    Alternative: SAP also ships a pure-Python DB-API2 driver, `sqlanydb`
    (pip install sqlanydb), which could replace pyodbc with minor changes
    to the connection layer only -- the SQL generated below is unaffected
    by that choice.

IMPORTANT VERSION CAVEAT:
SQL Anywhere's "Watcom-SQL" dialect has shifted somewhat across major
versions (9, 10, 11, 12, 16, 17 / SAP SQL Anywhere). The statements below
reflect the modern (v12+) documented syntax, but a few areas are genuinely
version-sensitive and are flagged inline with comments:
    - IF EXISTS support on DROP INDEX / DROP TABLE (v12+)
    - Whether index rebuild has a direct equivalent to Postgres REINDEX /
      SQL Server ALTER INDEX ... REBUILD (SQL Anywhere has no documented
      single-statement equivalent; this file rebuilds by dropping and
      recreating the index, which is always safe but takes a lock)
      the whole time, unlike a native online rebuild.
    - BACKUP DATABASE is a real SQL statement in SQL Anywhere, but there is
      no equivalent "RESTORE DATABASE" SQL statement -- restoring is
      normally done by stopping the server and replacing the .db file, or
      via the `dbrestore`/`dbeng` command-line utilities. `restore()` below
      shells out to `dbeng<version>` accordingly; adjust the executable
      name for your installed version.
Please confirm these against the SQL Anywhere Help for your specific
version before relying on this in production.

Note on the `rename` / `get_definition` signatures:
As in the other backend implementations in this project, this file follows
a "manager" style (one Index/Check/Column/Table instance can operate on any
object by name), so `rename` and `get_definition` accept explicit
identifying parameters instead of the single-argument, stateful signatures
declared in the base interface (database.py). This is a deliberate,
documented deviation kept consistent across all backends.
"""

import re
import subprocess
from typing import Any, Dict, List, Optional

import pyodbc

from database import Check, Column, Database, Index, Table


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def quote_ident(name: str) -> str:
    """Safely quotes an identifier using ANSI double-quote syntax, which
    SQL Anywhere uses by default when QUOTED_IDENTIFIER is ON (the default
    for ODBC connections)."""
    return '"' + str(name).replace('"', '""') + '"'


def quote_literal(value: Any) -> str:
    """Safely embeds a literal value into a DDL string."""
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def _named_to_qmark(sql_text: str, params: Optional[Dict[str, Any]]):
    """Converts a %(name)s-style query + params dict into pyodbc's qmark
    ('?') style, preserving parameter order of appearance."""
    if not params:
        return sql_text, []
    ordered_values: List[Any] = []

    def _replace(match: "re.Match") -> str:
        ordered_values.append(params[match.group(1)])
        return "?"

    converted = re.sub(r"%\((\w+)\)s", _replace, sql_text)
    return converted, ordered_values


# ---------------------------------------------------------------------------
# SQLAnywhereDatabase
# ---------------------------------------------------------------------------
class SQLAnywhereDatabase(Database):
    """SQL Anywhere implementation of the Database interface (pyodbc)."""

    def __init__(
        self,
        server: str,
        database: str,
        user: str = "dba",
        password: str = "sql",
        driver: str = "SQL Anywhere 17",
        host: Optional[str] = None,
        port: int = 2638,
    ):
        self.server = server          # SQL Anywhere "server name" (-n at startup)
        self.database = database      # database name (-n / DBN)
        self.user = user
        self.password = password
        self.driver = driver
        self.host = host or "localhost"
        self.port = port
        self.conn: Optional[pyodbc.Connection] = None
        self._last_error: Optional[str] = None

    def _build_conn_str(self, database: Optional[str] = None) -> str:
        db = database or self.database
        return (
            f"DRIVER={{{self.driver}}};"
            f"Host={self.host}:{self.port};"
            f"ServerName={self.server};"
            f"DatabaseName={db};"
            f"UID={self.user};PWD={self.password}"
        )

    # --- connection lifecycle ---
    def connect(self, **kwargs) -> bool:
        try:
            self.conn = pyodbc.connect(self._build_conn_str(), autocommit=True, **kwargs)
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def disconnect(self) -> bool:
        try:
            if self.conn is not None:
                self.conn.close()
                self.conn = None
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def is_connected(self) -> bool:
        if self.conn is None:
            return False
        try:
            self.conn.execute("SELECT 1")
            return True
        except Exception:
            return False

    # --- database-level operations ---
    def create(self, database_name: str, **kwargs) -> bool:
        """
        Creates a new SQL Anywhere database FILE (not just a schema/catalog
        as in Postgres/SQL Server -- SQL Anywhere databases are standalone
        .db files that then need to be started as a server to be usable).
        `kwargs` may include `file_path` (defaults to '<database_name>.db').
        """
        try:
            file_path = kwargs.get("file_path", f"{database_name}.db")
            self.conn.execute(
                "CREATE DATABASE ?", file_path,
            )
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def drop(self, database_name: str, **kwargs) -> bool:
        """
        SQL Anywhere has no "DROP DATABASE" SQL statement for a running
        database (a database is a file, not a catalog inside a running
        server as in Postgres/SQL Server). Dropping means stopping the
        server for that database and deleting the .db/.log files.
        `kwargs` should include `file_path` for this to do anything.
        """
        file_path = kwargs.get("file_path")
        if not file_path:
            self._last_error = (
                "SQL Anywhere has no DROP DATABASE statement; pass "
                "file_path=<path to .db file> and ensure the database is "
                "not running, then this will delete the file directly."
            )
            return False
        try:
            import os
            os.remove(file_path)
            log_path = file_path.rsplit(".", 1)[0] + ".log"
            if os.path.exists(log_path):
                os.remove(log_path)
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def exists(self, database_name: str) -> bool:
        """Checks if a database is currently running/registered on the server."""
        try:
            rows = self.execute_query(
                "SELECT 1 FROM sa_db_list() WHERE db_name = %(name)s",
                {"name": database_name},
            )
            return len(rows) > 0
        except Exception as exc:
            self._last_error = str(exc)
            return False

    # --- backup / restore ---
    def backup(self, destination_path: str, **kwargs) -> bool:
        """Uses SQL Anywhere's native BACKUP DATABASE SQL statement."""
        try:
            self.conn.execute(f"BACKUP DATABASE DIRECTORY {quote_literal(destination_path)}")
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def restore(self, backup_path: str, **kwargs) -> bool:
        """
        SQL Anywhere has no "RESTORE DATABASE" SQL statement. A backup
        taken with BACKUP DATABASE is already a consistent copy of the .db
        file, so "restoring" means stopping the server and starting it
        against the backup file (or copying it over the original).
        This method shells out to the `dbeng<version>` utility as a
        convenience wrapper; adjust `engine_cmd` in kwargs for your
        installed version (e.g. "dbeng17", "dbeng12").
        """
        try:
            engine_cmd = kwargs.get("engine_cmd", "dbeng17")
            cmd = [engine_cmd, backup_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                self._last_error = result.stderr
                return False
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    # --- raw SQL execution (accepts %(name)s-style queries, converted internally) ---
    def execute_sql(self, sql: str, params: Optional[Dict[str, Any]] = None) -> bool:
        try:
            converted, values = _named_to_qmark(sql, params)
            self.conn.execute(converted, values) if values else self.conn.execute(converted)
            if not self.conn.autocommit:
                self.conn.commit()
            return True
        except Exception as exc:
            self._last_error = str(exc)
            if not self.conn.autocommit:
                self.conn.rollback()
            return False

    def execute_query(
        self, sql: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        try:
            converted, values = _named_to_qmark(sql, params)
            cur = self.conn.execute(converted, values) if values else self.conn.execute(converted)
            columns = [col[0] for col in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
        except Exception as exc:
            self._last_error = str(exc)
            return []

    # --- transactions ---
    def begin_transaction(self) -> bool:
        try:
            self.conn.autocommit = False
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def commit(self) -> bool:
        try:
            self.conn.commit()
            self.conn.autocommit = True
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def rollback(self) -> bool:
        try:
            self.conn.rollback()
            self.conn.autocommit = True
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    # --- misc ---
    def get_version(self) -> str:
        cur = self.conn.execute("SELECT @@version")
        return cur.fetchone()[0]

    def get_last_error(self) -> Optional[str]:
        return self._last_error

    def health_check(self) -> bool:
        try:
            self.conn.execute("SELECT 1")
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False


# ---------------------------------------------------------------------------
# SQLAnywhereIndex
# ---------------------------------------------------------------------------
class SQLAnywhereIndex(Index):
    """SQL Anywhere implementation of the Index interface."""

    def __init__(self, database: SQLAnywhereDatabase):
        self.db = database

    def add(
        self,
        table: str,
        columns: List[str],
        unique: bool = False,
        index_type: Optional[str] = None,
        **kwargs,
    ) -> bool:
        try:
            index_name = kwargs.get("index_name") or f"idx_{table}_{'_'.join(columns)}"
            unique_kw = "UNIQUE " if unique else ""
            # SQL Anywhere index_type options are things like CLUSTERED /
            # NOT-CLUSTERED (rarely used); most indexes omit this entirely.
            type_kw = f"{index_type} " if index_type else ""
            cols_sql = ", ".join(quote_ident(c) for c in columns)
            query = (
                f"CREATE {unique_kw}{type_kw}INDEX {quote_ident(index_name)} "
                f"ON {quote_ident(table)} ({cols_sql})"
            )
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def drop(self, table: str, index_name: str, **kwargs) -> bool:
        try:
            # SQL Anywhere requires the index name to be qualified by table.
            # IF EXISTS requires SQL Anywhere 12+.
            self.db.conn.execute(
                f"DROP INDEX IF EXISTS {quote_ident(table)}.{quote_ident(index_name)}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def delete(self, table: str, index_name: str, **kwargs) -> bool:
        # An index holds no data of its own separate from its definition,
        # so "deleting" it is equivalent to dropping it.
        return self.drop(table, index_name, **kwargs)

    def update(self, table: str, index_name: str, **kwargs) -> bool:
        # No ALTER INDEX to change columns/uniqueness; drop and recreate.
        if not self.drop(table, index_name):
            return False
        columns = kwargs.pop("columns", [])
        unique = kwargs.pop("unique", False)
        index_type = kwargs.pop("index_type", None)
        kwargs["index_name"] = index_name
        return self.add(table, columns, unique=unique, index_type=index_type, **kwargs)

    def exists(self, table: str, index_name: str) -> bool:
        rows = self.db.execute_query(
            """
            SELECT 1 FROM SYSIDX i
            JOIN SYSTAB t ON t.table_id = i.table_id
            WHERE t.table_name = %(table)s AND i.index_name = %(index_name)s
            """,
            {"table": table, "index_name": index_name},
        )
        return len(rows) > 0

    def rename(self, table: str, old_name: str, new_name: str) -> bool:
        try:
            self.db.conn.execute(
                f"ALTER INDEX {quote_ident(old_name)} ON {quote_ident(table)} "
                f"RENAME TO {quote_ident(new_name)}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_definition(self, table: str, index_name: str) -> str:
        rows = self.db.execute_query(
            """
            SELECT i.index_name, i."unique", c.column_name, ic.sequence
            FROM SYSIDX i
            JOIN SYSTAB t ON t.table_id = i.table_id
            JOIN SYSIDXCOL ic ON ic.table_id = i.table_id AND ic.index_id = i.index_id
            JOIN SYSCOLUMN c ON c.table_id = ic.table_id AND c.column_id = ic.column_id
            WHERE t.table_name = %(table)s AND i.index_name = %(index_name)s
            ORDER BY ic.sequence
            """,
            {"table": table, "index_name": index_name},
        )
        if not rows:
            return ""
        unique = "UNIQUE " if rows[0]["unique"] else ""
        cols = ", ".join(r["column_name"] for r in rows)
        return f"CREATE {unique}INDEX {index_name} ON {table} ({cols})"

    # --- index-specific extras ---
    def rebuild(self, table: str, index_name: str) -> bool:
        """
        SQL Anywhere has no documented single-statement equivalent to
        Postgres REINDEX / SQL Server ALTER INDEX...REBUILD, so this is
        implemented as drop + recreate (safe, but blocking for the duration).
        """
        definition = self.get_definition(table, index_name)
        if not definition:
            self.db._last_error = f"Index {index_name} not found on {table}"
            return False
        if not self.drop(table, index_name):
            return False
        try:
            self.db.conn.execute(definition)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_usage_stats(self, table: str, index_name: str) -> Dict[str, Any]:
        # SQL Anywhere exposes index statistics via the sa_index_density() /
        # sa_table_page_usage() procedures rather than a running counter
        # table like Postgres's pg_stat_user_indexes; this returns density
        # as an approximate usefulness signal instead of scan counts.
        rows = self.db.execute_query(
            """
            SELECT IndexName AS index_name, Density AS density
            FROM sa_index_density(%(table)s)
            WHERE IndexName = %(index_name)s
            """,
            {"table": table, "index_name": index_name},
        )
        return rows[0] if rows else {}

    def list_by_table(self, table: str) -> List[str]:
        rows = self.db.execute_query(
            """
            SELECT DISTINCT i.index_name
            FROM SYSIDX i
            JOIN SYSTAB t ON t.table_id = i.table_id
            WHERE t.table_name = %(table)s AND i.index_name IS NOT NULL
            """,
            {"table": table},
        )
        return [row["index_name"] for row in rows]


# ---------------------------------------------------------------------------
# SQLAnywhereCheck
# ---------------------------------------------------------------------------
class SQLAnywhereCheck(Check):
    """SQL Anywhere implementation of the Check interface (CHECK constraints)."""

    def __init__(self, database: SQLAnywhereDatabase):
        self.db = database

    def add(self, table: str, constraint_name: str, expression: str, **kwargs) -> bool:
        try:
            query = (
                f"ALTER TABLE {quote_ident(table)} "
                f"ADD CONSTRAINT {quote_ident(constraint_name)} CHECK ({expression})"
            )
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def drop(self, table: str, constraint_name: str, **kwargs) -> bool:
        try:
            self.db.conn.execute(
                f"ALTER TABLE {quote_ident(table)} DROP CONSTRAINT {quote_ident(constraint_name)}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def delete(self, table: str, constraint_name: str, **kwargs) -> bool:
        # A CHECK constraint has no data of its own; deleting == dropping it.
        return self.drop(table, constraint_name, **kwargs)

    def update(self, table: str, constraint_name: str, **kwargs) -> bool:
        expression = kwargs.pop("expression", None)
        if expression is None:
            self.db._last_error = "update() requires an 'expression' argument"
            return False
        if not self.drop(table, constraint_name):
            return False
        return self.add(table, constraint_name, expression, **kwargs)

    def exists(self, table: str, constraint_name: str) -> bool:
        rows = self.db.execute_query(
            """
            SELECT 1 FROM SYSCONSTRAINT sc
            JOIN SYSTABLE st ON st.object_id = sc.table_object_id
            WHERE st.table_name = %(table)s AND sc.constraint_name = %(name)s
            """,
            {"table": table, "name": constraint_name},
        )
        return len(rows) > 0

    def rename(self, table: str, old_name: str, new_name: str) -> bool:
        # SQL Anywhere has no documented ALTER ... RENAME CONSTRAINT;
        # rename via drop + re-add is the only portable option.
        definition = self.get_definition(table, old_name)
        if not definition:
            self.db._last_error = f"Constraint {old_name} not found on {table}"
            return False
        if not self.drop(table, old_name):
            return False
        return self.add(table, new_name, definition)

    def get_definition(self, table: str, constraint_name: str) -> str:
        rows = self.db.execute_query(
            """
            SELECT sc."check" AS definition
            FROM SYSCONSTRAINT sc
            JOIN SYSTABLE st ON st.object_id = sc.table_object_id
            WHERE st.table_name = %(table)s AND sc.constraint_name = %(name)s
            """,
            {"table": table, "name": constraint_name},
        )
        return rows[0]["definition"] if rows else ""

    # --- check-specific extras ---
    def enable(self, table: str, constraint_name: str) -> bool:
        # SQL Anywhere has no native disable/enable toggle for CHECK
        # constraints (same limitation as PostgreSQL); drop/add is the
        # only option, so this is a no-op success if the constraint exists.
        return self.exists(table, constraint_name)

    def disable(self, table: str, constraint_name: str) -> bool:
        self.db._last_error = (
            "SQL Anywhere does not support disabling CHECK constraints; "
            "drop() is the only option"
        )
        return False

    def validate(self, table: str, constraint_name: str) -> bool:
        # Constraints are always enforced immediately when added in SQL
        # Anywhere (no NOT VALID concept); nothing to validate separately.
        return self.exists(table, constraint_name)


# ---------------------------------------------------------------------------
# SQLAnywhereColumn
# ---------------------------------------------------------------------------
class SQLAnywhereColumn(Column):
    """SQL Anywhere implementation of the Column interface."""

    def __init__(self, database: SQLAnywhereDatabase):
        self.db = database

    def add(
        self,
        table: str,
        column_name: str,
        data_type: str,
        nullable: bool = True,
        default: Optional[Any] = None,
        **kwargs,
    ) -> bool:
        try:
            not_null = "" if nullable else " NOT NULL"
            default_clause = f" DEFAULT {quote_literal(default)}" if default is not None else ""
            query = (
                f"ALTER TABLE {quote_ident(table)} ADD {quote_ident(column_name)} "
                f"{data_type}{default_clause}{not_null}"
            )
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def drop(self, table: str, column_name: str, **kwargs) -> bool:
        try:
            self.db.conn.execute(
                f"ALTER TABLE {quote_ident(table)} DROP COLUMN {quote_ident(column_name)}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def delete(self, table: str, column_name: str, **kwargs) -> bool:
        """Clears the column's values (sets them to NULL) without dropping it."""
        try:
            self.db.conn.execute(
                f"UPDATE {quote_ident(table)} SET {quote_ident(column_name)} = NULL"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def update(self, table: str, column_name: str, **kwargs) -> bool:
        """
        Applies one or more column alterations based on the keyword
        arguments provided: new_type, default, nullable, new_name.
        """
        ok = True
        if "new_type" in kwargs:
            ok = ok and self.change_type(table, column_name, kwargs["new_type"])
        if "default" in kwargs:
            ok = ok and self.set_default(table, column_name, kwargs["default"])
        if "nullable" in kwargs:
            ok = ok and self.set_nullable(table, column_name, kwargs["nullable"])
        if "new_name" in kwargs:
            ok = ok and self.rename(table, column_name, kwargs["new_name"])
        return ok

    def exists(self, table: str, column_name: str) -> bool:
        rows = self.db.execute_query(
            """
            SELECT 1 FROM SYSCOLUMN c
            JOIN SYSTAB t ON t.table_id = c.table_id
            WHERE t.table_name = %(table)s AND c.column_name = %(col)s
            """,
            {"table": table, "col": column_name},
        )
        return len(rows) > 0

    def rename(self, table: str, old_name: str, new_name: str) -> bool:
        try:
            self.db.conn.execute(
                f"ALTER TABLE {quote_ident(table)} RENAME {quote_ident(old_name)} TO {quote_ident(new_name)}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_definition(self, table: str, column_name: str) -> str:
        rows = self.db.execute_query(
            """
            SELECT c.column_name, c.domain_name AS data_type, c.nulls, c."default"
            FROM SYSCOLUMN c
            JOIN SYSTAB t ON t.table_id = c.table_id
            WHERE t.table_name = %(table)s AND c.column_name = %(col)s
            """,
            {"table": table, "col": column_name},
        )
        if not rows:
            return ""
        row = rows[0]
        nullable = "" if row["nulls"] == "Y" else " NOT NULL"
        default = f" DEFAULT {row['default']}" if row["default"] else ""
        return f"{row['column_name']} {row['data_type']}{default}{nullable}"

    # --- column-specific extras ---
    # SQL Anywhere's ALTER TABLE ... ALTER COLUMN accepts granular clauses
    # (type / NULL-ability / default) independently, unlike SQL Server,
    # which requires restating the full column definition each time.
    def change_type(self, table: str, column_name: str, new_type: str) -> bool:
        try:
            self.db.conn.execute(
                f"ALTER TABLE {quote_ident(table)} ALTER {quote_ident(column_name)} {new_type}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def set_default(self, table: str, column_name: str, default: Any) -> bool:
        try:
            if default is None:
                query = (
                    f"ALTER TABLE {quote_ident(table)} "
                    f"ALTER {quote_ident(column_name)} DROP DEFAULT"
                )
            else:
                query = (
                    f"ALTER TABLE {quote_ident(table)} "
                    f"ALTER {quote_ident(column_name)} SET DEFAULT {quote_literal(default)}"
                )
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def set_nullable(self, table: str, column_name: str, nullable: bool) -> bool:
        try:
            null_clause = "NULL" if nullable else "NOT NULL"
            self.db.conn.execute(
                f"ALTER TABLE {quote_ident(table)} ALTER {quote_ident(column_name)} {null_clause}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def list_by_table(self, table: str) -> List[Dict[str, Any]]:
        return self.db.execute_query(
            """
            SELECT c.column_name, c.domain_name AS data_type, c.nulls, c."default"
            FROM SYSCOLUMN c
            JOIN SYSTAB t ON t.table_id = c.table_id
            WHERE t.table_name = %(table)s
            ORDER BY c.column_id
            """,
            {"table": table},
        )


# ---------------------------------------------------------------------------
# SQLAnywhereTable
# ---------------------------------------------------------------------------
class SQLAnywhereTable(Table):
    """SQL Anywhere implementation of the Table interface."""

    def __init__(self, database: SQLAnywhereDatabase):
        self.db = database

    def add(self, table_name: str, columns: List[Dict[str, Any]], **kwargs) -> bool:
        """
        columns: list of dicts, e.g.
            [{"name": "id", "type": "INTEGER DEFAULT AUTOINCREMENT", "primary_key": True},
             {"name": "email", "type": "VARCHAR(255)", "nullable": False}]

        Note: SQL Anywhere has no IDENTITY keyword like SQL Server; use
        "DEFAULT AUTOINCREMENT" (or "DEFAULT GLOBAL AUTOINCREMENT" for
        replicated/synchronized databases) as the column's `type`/default.
        """
        try:
            column_defs = []
            pk_columns = []
            for col in columns:
                parts = [quote_ident(col["name"]), col["type"]]
                if not col.get("nullable", True):
                    parts.append("NOT NULL")
                if col.get("default") is not None:
                    parts.append(f"DEFAULT {quote_literal(col['default'])}")
                column_defs.append(" ".join(parts))
                if col.get("primary_key"):
                    pk_columns.append(col["name"])

            if pk_columns:
                pk_cols_sql = ", ".join(quote_ident(c) for c in pk_columns)
                column_defs.append(f"PRIMARY KEY ({pk_cols_sql})")

            query = f"CREATE TABLE {quote_ident(table_name)} ({', '.join(column_defs)})"
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def drop(self, table_name: str, **kwargs) -> bool:
        try:
            # IF EXISTS requires SQL Anywhere 12+.
            self.db.conn.execute(f"DROP TABLE IF EXISTS {quote_ident(table_name)}")
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def delete(self, table_name: str, where: Optional[str] = None, **kwargs) -> bool:
        try:
            where_clause = f" WHERE {where}" if where else ""
            self.db.conn.execute(f"DELETE FROM {quote_ident(table_name)}{where_clause}")
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def update(self, table_name: str, **kwargs) -> bool:
        """
        Updates rows. Expects:
            set: Dict[str, Any]  -- columns and new values
            where: Optional[str] -- raw WHERE clause (no bind params, kept simple)
        """
        try:
            values = kwargs.get("set")
            where = kwargs.get("where")
            if not values:
                self.db._last_error = "update() requires a 'set' dict with column/value pairs"
                return False

            set_parts = [f"{quote_ident(col)} = {quote_literal(val)}" for col, val in values.items()]
            where_clause = f" WHERE {where}" if where else ""
            query = f"UPDATE {quote_ident(table_name)} SET {', '.join(set_parts)}{where_clause}"
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def exists(self, table_name: str) -> bool:
        rows = self.db.execute_query(
            "SELECT 1 FROM SYSTAB WHERE table_name = %(name)s AND table_type = 'BASE'",
            {"name": table_name},
        )
        return len(rows) > 0

    def rename(self, table_name: str, new_name: str) -> bool:
        try:
            # Note: no "TO" keyword in SQL Anywhere's ALTER TABLE...RENAME.
            self.db.conn.execute(
                f"ALTER TABLE {quote_ident(table_name)} RENAME {quote_ident(new_name)}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_definition(self, table_name: str) -> str:
        """Builds a simplified CREATE TABLE statement from catalog metadata."""
        columns = self.db.execute_query(
            """
            SELECT c.column_name, c.domain_name AS data_type, c.nulls, c."default"
            FROM SYSCOLUMN c
            JOIN SYSTAB t ON t.table_id = c.table_id
            WHERE t.table_name = %(name)s
            ORDER BY c.column_id
            """,
            {"name": table_name},
        )
        if not columns:
            return ""

        lines = []
        for col in columns:
            line = f"{col['column_name']} {col['data_type']}"
            if col["default"]:
                line += f" DEFAULT {col['default']}"
            if col["nulls"] == "N":
                line += " NOT NULL"
            lines.append(line)

        return f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(lines) + "\n);"

    # --- table-specific extras ---
    def truncate(self, table_name: str) -> bool:
        try:
            self.db.conn.execute(f"TRUNCATE TABLE {quote_ident(table_name)}")
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def count_rows(self, table_name: str, where: Optional[str] = None) -> int:
        where_sql = f" WHERE {where}" if where else ""
        rows = self.db.execute_query(f"SELECT COUNT(*) AS total FROM {quote_ident(table_name)}{where_sql}")
        return rows[0]["total"] if rows else 0

    def get_primary_key(self, table_name: str) -> List[str]:
        rows = self.db.execute_query(
            """
            SELECT c.column_name
            FROM SYSIDX i
            JOIN SYSIDXCOL ic ON ic.table_id = i.table_id AND ic.index_id = i.index_id
            JOIN SYSCOLUMN c ON c.table_id = ic.table_id AND c.column_id = ic.column_id
            JOIN SYSTAB t ON t.table_id = i.table_id
            WHERE t.table_name = %(table)s AND i.index_category = 1
            ORDER BY ic.sequence
            """,
            {"table": table_name},
        )
        return [row["column_name"] for row in rows]
        # index_category = 1 identifies the primary key index in SYSIDX.

    def get_foreign_keys(self, table_name: str) -> List[Dict[str, Any]]:
        return self.db.execute_query(
            """
            SELECT
                fk.role AS constraint_name,
                pc.column_name,
                ft.table_name AS foreign_table_name,
                fc.column_name AS foreign_column_name
            FROM SYSFKEY fk
            JOIN SYSTAB pt ON pt.table_id = fk.foreign_table_id
            JOIN SYSTAB ft ON ft.table_id = fk.primary_table_id
            JOIN SYSFKCOL fkc ON fkc.foreign_table_id = fk.foreign_table_id AND fkc.foreign_key_id = fk.foreign_key_id
            JOIN SYSCOLUMN pc ON pc.table_id = fkc.foreign_table_id AND pc.column_id = fkc.foreign_column_id
            JOIN SYSCOLUMN fc ON fc.table_id = fkc.primary_table_id AND fc.column_id = fkc.primary_column_id
            WHERE pt.table_name = %(table)s
            """,
            {"table": table_name},
        )

    def list_tables(self, schema: Optional[str] = None) -> List[str]:
        # SQL Anywhere organizes tables by "creator"/user id rather than a
        # schema name string as in Postgres/SQL Server; when provided,
        # `schema` is matched against the owning user name.
        if schema:
            rows = self.db.execute_query(
                """
                SELECT t.table_name
                FROM SYSTAB t
                JOIN SYSUSER u ON u.user_id = t.creator
                WHERE u.user_name = %(schema)s AND t.table_type = 'BASE'
                """,
                {"schema": schema},
            )
        else:
            rows = self.db.execute_query(
                "SELECT table_name FROM SYSTAB WHERE table_type = 'BASE'"
            )
        return [row["table_name"] for row in rows]


# ---------------------------------------------------------------------------
# Usage example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    db = SQLAnywhereDatabase(
        server="my_asa_server", database="my_app",
        user="dba", password="sql", host="localhost", port=2638,
    )
    if db.connect():
        table = SQLAnywhereTable(db)
        column = SQLAnywhereColumn(db)
        index = SQLAnywhereIndex(db)
        check = SQLAnywhereCheck(db)

        table.add("customers", [
            {"name": "id", "type": "INTEGER DEFAULT AUTOINCREMENT", "primary_key": True},
            {"name": "name", "type": "VARCHAR(255)", "nullable": False},
            {"name": "email", "type": "VARCHAR(255)", "nullable": False},
            {"name": "age", "type": "INTEGER"},
        ])

        column.add("customers", "created_at", "TIMESTAMP", default="CURRENT TIMESTAMP")
        index.add("customers", ["email"], unique=True)
        check.add("customers", "chk_age_positive", "age >= 0")

        print(table.get_definition("customers"))
        print(index.list_by_table("customers"))

        db.disconnect()
    else:
        print("Connection failed:", db.get_last_error())