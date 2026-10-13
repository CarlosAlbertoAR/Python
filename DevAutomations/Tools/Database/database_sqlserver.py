"""
sqlserver_database.py

SQL Server implementation of the interfaces defined in database.py
(Database, Index, Check, Column, Table), using pyodbc.

Requirements:
    pip install pyodbc
    A SQL Server ODBC driver installed on the host machine
    (e.g. "ODBC Driver 17 for SQL Server" or "ODBC Driver 18 for SQL Server").

Notes / T-SQL-specific decisions:
- pyodbc has no query-building helper like psycopg's `sql` module, so
  identifiers are quoted manually with `quote_ident()` ([brackets], with
  internal `]` doubled) and literal values with `quote_literal()`.
- pyodbc uses positional "?" placeholders, not the %(name)s style used by
  the Postgres implementations. To keep the manager-style API identical
  across all Database implementations, `execute_sql` / `execute_query`
  still accept %(name)s-style queries and a params dict; internally they
  are converted to qmark style via `_named_to_qmark()`.
- Unlike PostgreSQL, SQL Server natively supports enabling/disabling CHECK
  constraints without dropping them (`NOCHECK CONSTRAINT` / `WITH CHECK
  CHECK CONSTRAINT`), so `Check.disable()` is fully implemented here.
- `rename` in SQL Server is done via the `sp_rename` system procedure, not
  an ALTER TABLE/INDEX RENAME clause.
- `STRING_AGG` (used in Index.get_definition) requires SQL Server 2017+.
  `DROP TABLE IF EXISTS` / `DROP INDEX IF EXISTS` require SQL Server 2016+.

Note on the `rename` / `get_definition` signatures:
As in the Postgres implementations, this file follows a "manager" style
(one Index/Check/Column/Table instance can operate on any object by name),
so `rename` and `get_definition` accept explicit identifying parameters
instead of the single-argument, stateful signatures declared in the base
interface (database.py). This is a deliberate, documented deviation kept
consistent with the other backend implementations.
"""

import re
from typing import Any, Dict, List, Optional

import pyodbc

from database import Check, Column, Database, Index, Table


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def quote_ident(name: str) -> str:
    """Safely quotes an identifier using T-SQL square-bracket syntax."""
    return "[" + str(name).replace("]", "]]") + "]"


def quote_literal(value: Any) -> str:
    """Safely embeds a literal value into a DDL string (T-SQL escaping)."""
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
# SQLServerDatabase
# ---------------------------------------------------------------------------
class SQLServerDatabase(Database):
    """SQL Server implementation of the Database interface (pyodbc)."""

    def __init__(
        self,
        server: str,
        database: str = "master",
        user: Optional[str] = None,
        password: Optional[str] = None,
        driver: str = "ODBC Driver 17 for SQL Server",
        port: int = 1433,
        trusted_connection: bool = False,
    ):
        self.server = server
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.driver = driver
        self.trusted_connection = trusted_connection
        self.conn: Optional[pyodbc.Connection] = None
        self._last_error: Optional[str] = None

    def _build_conn_str(self, database: Optional[str] = None) -> str:
        db = database or self.database
        parts = [
            f"DRIVER={{{self.driver}}}",
            f"SERVER={self.server},{self.port}",
            f"DATABASE={db}",
        ]
        if self.trusted_connection:
            parts.append("Trusted_Connection=yes")
        else:
            parts.append(f"UID={self.user}")
            parts.append(f"PWD={self.password}")
        return ";".join(parts)

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

    def _maintenance_connection(self) -> pyodbc.Connection:
        """Opens a short-lived autocommit connection to 'master' (CREATE
        DATABASE / DROP DATABASE cannot run inside a transaction block, and
        can't target the database currently in use)."""
        return pyodbc.connect(self._build_conn_str(database="master"), autocommit=True)

    # --- database-level operations ---
    def create(self, database_name: str, **kwargs) -> bool:
        try:
            conn = self._maintenance_connection()
            conn.execute(f"CREATE DATABASE {quote_ident(database_name)}")
            conn.close()
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def drop(self, database_name: str, **kwargs) -> bool:
        try:
            conn = self._maintenance_connection()
            conn.execute(
                f"IF DB_ID({quote_literal(database_name)}) IS NOT NULL "
                f"ALTER DATABASE {quote_ident(database_name)} SET SINGLE_USER WITH ROLLBACK IMMEDIATE"
            )
            conn.execute(f"DROP DATABASE IF EXISTS {quote_ident(database_name)}")
            conn.close()
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def exists(self, database_name: str) -> bool:
        try:
            conn = self._maintenance_connection()
            cur = conn.execute("SELECT 1 FROM sys.databases WHERE name = ?", database_name)
            found = cur.fetchone() is not None
            conn.close()
            return found
        except Exception as exc:
            self._last_error = str(exc)
            return False

    # --- backup / restore (native T-SQL BACKUP/RESTORE) ---
    def backup(self, destination_path: str, **kwargs) -> bool:
        try:
            self.conn.execute(
                f"BACKUP DATABASE {quote_ident(self.database)} TO DISK = ?", destination_path
            )
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def restore(self, backup_path: str, **kwargs) -> bool:
        try:
            conn = self._maintenance_connection()
            conn.execute(
                f"ALTER DATABASE {quote_ident(self.database)} SET SINGLE_USER WITH ROLLBACK IMMEDIATE"
            )
            conn.execute(
                f"RESTORE DATABASE {quote_ident(self.database)} FROM DISK = ? WITH REPLACE",
                backup_path,
            )
            conn.execute(f"ALTER DATABASE {quote_ident(self.database)} SET MULTI_USER")
            conn.close()
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    # --- raw SQL execution (accepts %(name)s-style queries, see module docstring) ---
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
        cur = self.conn.execute("SELECT @@VERSION")
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
# SQLServerIndex
# ---------------------------------------------------------------------------
class SQLServerIndex(Index):
    """SQL Server implementation of the Index interface."""

    def __init__(self, database: SQLServerDatabase):
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
            # index_type here means CLUSTERED / NONCLUSTERED (SQL Server has
            # no direct equivalent to Postgres access methods like btree/gin)
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
            # SQL Server requires the table name for DROP INDEX
            self.db.conn.execute(
                f"DROP INDEX IF EXISTS {quote_ident(index_name)} ON {quote_ident(table)}"
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
        # SQL Server has no direct way to change columns/uniqueness of an
        # existing index; drop and recreate with the new definition.
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
            SELECT 1 FROM sys.indexes i
            JOIN sys.tables t ON t.object_id = i.object_id
            WHERE t.name = %(table)s AND i.name = %(index_name)s
            """,
            {"table": table, "index_name": index_name},
        )
        return len(rows) > 0

    def rename(self, table: str, old_name: str, new_name: str) -> bool:
        try:
            self.db.conn.execute("EXEC sp_rename ?, ?, N'INDEX'", f"{table}.{old_name}", new_name)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_definition(self, table: str, index_name: str) -> str:
        # Requires SQL Server 2017+ (STRING_AGG)
        rows = self.db.execute_query(
            """
            SELECT i.name AS index_name, i.is_unique, i.type_desc,
                   STRING_AGG(c.name, ', ') WITHIN GROUP (ORDER BY ic.key_ordinal) AS cols
            FROM sys.indexes i
            JOIN sys.tables t ON t.object_id = i.object_id
            JOIN sys.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id
            JOIN sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
            WHERE t.name = %(table)s AND i.name = %(index_name)s
            GROUP BY i.name, i.is_unique, i.type_desc
            """,
            {"table": table, "index_name": index_name},
        )
        if not rows:
            return ""
        row = rows[0]
        unique = "UNIQUE " if row["is_unique"] else ""
        return f"CREATE {unique}{row['type_desc']} INDEX {row['index_name']} ON {table} ({row['cols']})"

    # --- index-specific extras ---
    def rebuild(self, table: str, index_name: str) -> bool:
        try:
            self.db.conn.execute(
                f"ALTER INDEX {quote_ident(index_name)} ON {quote_ident(table)} REBUILD"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_usage_stats(self, table: str, index_name: str) -> Dict[str, Any]:
        rows = self.db.execute_query(
            """
            SELECT s.user_seeks, s.user_scans, s.user_lookups, s.user_updates
            FROM sys.dm_db_index_usage_stats s
            JOIN sys.indexes i ON i.object_id = s.object_id AND i.index_id = s.index_id
            JOIN sys.tables t ON t.object_id = s.object_id
            WHERE t.name = %(table)s AND i.name = %(index_name)s AND s.database_id = DB_ID()
            """,
            {"table": table, "index_name": index_name},
        )
        return rows[0] if rows else {}

    def list_by_table(self, table: str) -> List[str]:
        rows = self.db.execute_query(
            """
            SELECT i.name AS index_name
            FROM sys.indexes i
            JOIN sys.tables t ON t.object_id = i.object_id
            WHERE t.name = %(table)s AND i.name IS NOT NULL
            """,
            {"table": table},
        )
        return [row["index_name"] for row in rows]


# ---------------------------------------------------------------------------
# SQLServerCheck
# ---------------------------------------------------------------------------
class SQLServerCheck(Check):
    """SQL Server implementation of the Check interface (CHECK constraints)."""

    def __init__(self, database: SQLServerDatabase):
        self.db = database

    def add(self, table: str, constraint_name: str, expression: str, **kwargs) -> bool:
        try:
            with_nocheck = "WITH NOCHECK " if kwargs.get("not_valid") else ""
            query = (
                f"ALTER TABLE {quote_ident(table)} {with_nocheck}"
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
                f"ALTER TABLE {quote_ident(table)} DROP CONSTRAINT IF EXISTS {quote_ident(constraint_name)}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def delete(self, table: str, constraint_name: str, **kwargs) -> bool:
        # A CHECK constraint has no data of its own; deleting == dropping it.
        return self.drop(table, constraint_name, **kwargs)

    def update(self, table: str, constraint_name: str, **kwargs) -> bool:
        # SQL Server has no ALTER CONSTRAINT to change a CHECK expression;
        # drop and re-add with the new expression.
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
            SELECT 1 FROM sys.check_constraints cc
            JOIN sys.tables t ON t.object_id = cc.parent_object_id
            WHERE t.name = %(table)s AND cc.name = %(name)s
            """,
            {"table": table, "name": constraint_name},
        )
        return len(rows) > 0

    def rename(self, table: str, old_name: str, new_name: str) -> bool:
        try:
            self.db.conn.execute("EXEC sp_rename ?, ?, N'OBJECT'", old_name, new_name)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_definition(self, table: str, constraint_name: str) -> str:
        rows = self.db.execute_query(
            """
            SELECT cc.definition
            FROM sys.check_constraints cc
            JOIN sys.tables t ON t.object_id = cc.parent_object_id
            WHERE t.name = %(table)s AND cc.name = %(name)s
            """,
            {"table": table, "name": constraint_name},
        )
        return rows[0]["definition"] if rows else ""

    # --- check-specific extras ---
    # Unlike PostgreSQL, SQL Server natively supports enabling/disabling
    # CHECK constraints without dropping them.
    def enable(self, table: str, constraint_name: str) -> bool:
        return self.validate(table, constraint_name)

    def disable(self, table: str, constraint_name: str) -> bool:
        try:
            self.db.conn.execute(
                f"ALTER TABLE {quote_ident(table)} NOCHECK CONSTRAINT {quote_ident(constraint_name)}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def validate(self, table: str, constraint_name: str) -> bool:
        try:
            # WITH CHECK re-enables the constraint AND validates existing data
            self.db.conn.execute(
                f"ALTER TABLE {quote_ident(table)} WITH CHECK CHECK CONSTRAINT {quote_ident(constraint_name)}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False


# ---------------------------------------------------------------------------
# SQLServerColumn
# ---------------------------------------------------------------------------
class SQLServerColumn(Column):
    """SQL Server implementation of the Column interface."""

    def __init__(self, database: SQLServerDatabase):
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
            self._drop_default_constraint(table, column_name)
            self.db.conn.execute(
                f"ALTER TABLE {quote_ident(table)} DROP COLUMN {quote_ident(column_name)}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def _drop_default_constraint(self, table: str, column_name: str) -> None:
        """SQL Server auto-names DEFAULT constraints; they must be dropped
        explicitly before dropping the column or changing its default."""
        rows = self.db.execute_query(
            """
            SELECT dc.name
            FROM sys.default_constraints dc
            JOIN sys.columns c ON c.object_id = dc.parent_object_id AND c.column_id = dc.parent_column_id
            JOIN sys.tables t ON t.object_id = dc.parent_object_id
            WHERE t.name = %(table)s AND c.name = %(col)s
            """,
            {"table": table, "col": column_name},
        )
        for row in rows:
            self.db.conn.execute(
                f"ALTER TABLE {quote_ident(table)} DROP CONSTRAINT {quote_ident(row['name'])}"
            )

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
        Applies one or more column alterations based on the keyword arguments
        provided: new_type, default, nullable, new_name.
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
            SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = %(table)s AND COLUMN_NAME = %(col)s
            """,
            {"table": table, "col": column_name},
        )
        return len(rows) > 0

    def rename(self, table: str, old_name: str, new_name: str) -> bool:
        try:
            self.db.conn.execute("EXEC sp_rename ?, ?, N'COLUMN'", f"{table}.{old_name}", new_name)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_definition(self, table: str, column_name: str) -> str:
        rows = self.db.execute_query(
            """
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = %(table)s AND COLUMN_NAME = %(col)s
            """,
            {"table": table, "col": column_name},
        )
        if not rows:
            return ""
        row = rows[0]
        nullable = "" if row["IS_NULLABLE"] == "YES" else " NOT NULL"
        default = f" DEFAULT {row['COLUMN_DEFAULT']}" if row["COLUMN_DEFAULT"] else ""
        return f"{row['COLUMN_NAME']} {row['DATA_TYPE']}{default}{nullable}"

    # --- column-specific extras ---
    def change_type(self, table: str, column_name: str, new_type: str, nullable: Optional[bool] = None) -> bool:
        try:
            # SQL Server requires nullability to be restated on ALTER COLUMN;
            # if not provided, the current NOT NULL/NULL setting is preserved.
            null_clause = ""
            if nullable is not None:
                null_clause = " NULL" if nullable else " NOT NULL"
            self.db.conn.execute(
                f"ALTER TABLE {quote_ident(table)} ALTER COLUMN {quote_ident(column_name)} {new_type}{null_clause}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def set_default(self, table: str, column_name: str, default: Any) -> bool:
        try:
            self._drop_default_constraint(table, column_name)
            if default is not None:
                constraint_name = f"DF_{table}_{column_name}"
                self.db.conn.execute(
                    f"ALTER TABLE {quote_ident(table)} ADD CONSTRAINT {quote_ident(constraint_name)} "
                    f"DEFAULT {quote_literal(default)} FOR {quote_ident(column_name)}"
                )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def set_nullable(self, table: str, column_name: str, nullable: bool) -> bool:
        try:
            # ALTER COLUMN requires restating the data type, so it is looked
            # up first from INFORMATION_SCHEMA.
            rows = self.db.execute_query(
                """
                SELECT DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = %(table)s AND COLUMN_NAME = %(col)s
                """,
                {"table": table, "col": column_name},
            )
            if not rows:
                self.db._last_error = "Column not found"
                return False
            row = rows[0]
            data_type = row["DATA_TYPE"]
            if row["CHARACTER_MAXIMUM_LENGTH"]:
                length = row["CHARACTER_MAXIMUM_LENGTH"]
                length_sql = "MAX" if length == -1 else str(length)
                data_type = f"{data_type}({length_sql})"
            elif row["NUMERIC_PRECISION"] and data_type.lower() in ("decimal", "numeric"):
                data_type = f"{data_type}({row['NUMERIC_PRECISION']},{row['NUMERIC_SCALE']})"

            null_clause = "NULL" if nullable else "NOT NULL"
            self.db.conn.execute(
                f"ALTER TABLE {quote_ident(table)} ALTER COLUMN {quote_ident(column_name)} {data_type} {null_clause}"
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def list_by_table(self, table: str) -> List[Dict[str, Any]]:
        return self.db.execute_query(
            """
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = %(table)s
            ORDER BY ORDINAL_POSITION
            """,
            {"table": table},
        )


# ---------------------------------------------------------------------------
# SQLServerTable
# ---------------------------------------------------------------------------
class SQLServerTable(Table):
    """SQL Server implementation of the Table interface."""

    def __init__(self, database: SQLServerDatabase):
        self.db = database

    def add(self, table_name: str, columns: List[Dict[str, Any]], **kwargs) -> bool:
        """
        columns: list of dicts, e.g.
            [{"name": "id", "type": "INT IDENTITY(1,1)", "primary_key": True},
             {"name": "email", "type": "VARCHAR(255)", "nullable": False}]
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
            "SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = %(name)s",
            {"name": table_name},
        )
        return len(rows) > 0

    def rename(self, table_name: str, new_name: str) -> bool:
        try:
            self.db.conn.execute("EXEC sp_rename ?, ?", table_name, new_name)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_definition(self, table_name: str) -> str:
        """Builds a simplified CREATE TABLE statement from catalog metadata."""
        columns = self.db.execute_query(
            """
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = %(name)s
            ORDER BY ORDINAL_POSITION
            """,
            {"name": table_name},
        )
        if not columns:
            return ""

        lines = []
        for col in columns:
            line = f"{col['COLUMN_NAME']} {col['DATA_TYPE']}"
            if col["COLUMN_DEFAULT"]:
                line += f" DEFAULT {col['COLUMN_DEFAULT']}"
            if col["IS_NULLABLE"] == "NO":
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
            SELECT c.name AS column_name
            FROM sys.indexes i
            JOIN sys.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id
            JOIN sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
            JOIN sys.tables t ON t.object_id = i.object_id
            WHERE t.name = %(table)s AND i.is_primary_key = 1
            ORDER BY ic.key_ordinal
            """,
            {"table": table_name},
        )
        return [row["column_name"] for row in rows]

    def get_foreign_keys(self, table_name: str) -> List[Dict[str, Any]]:
        return self.db.execute_query(
            """
            SELECT
                fk.name AS constraint_name,
                cpa.name AS column_name,
                tr.name AS foreign_table_name,
                cref.name AS foreign_column_name
            FROM sys.foreign_keys fk
            JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
            JOIN sys.tables tp ON tp.object_id = fk.parent_object_id
            JOIN sys.tables tr ON tr.object_id = fk.referenced_object_id
            JOIN sys.columns cpa ON cpa.object_id = fkc.parent_object_id AND cpa.column_id = fkc.parent_column_id
            JOIN sys.columns cref ON cref.object_id = fkc.referenced_object_id AND cref.column_id = fkc.referenced_column_id
            WHERE tp.name = %(table)s
            """,
            {"table": table_name},
        )

    def list_tables(self, schema: Optional[str] = None) -> List[str]:
        schema = schema or "dbo"
        rows = self.db.execute_query(
            """
            SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = %(schema)s AND TABLE_TYPE = 'BASE TABLE'
            """,
            {"schema": schema},
        )
        return [row["TABLE_NAME"] for row in rows]


# ---------------------------------------------------------------------------
# Usage example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    db = SQLServerDatabase(
        server="localhost", database="my_app",
        user="sa", password="YourStrong!Passw0rd",
    )
    if db.connect():
        table = SQLServerTable(db)
        column = SQLServerColumn(db)
        index = SQLServerIndex(db)
        check = SQLServerCheck(db)

        table.add("customers", [
            {"name": "id", "type": "INT IDENTITY(1,1)", "primary_key": True},
            {"name": "name", "type": "VARCHAR(255)", "nullable": False},
            {"name": "email", "type": "VARCHAR(255)", "nullable": False},
            {"name": "age", "type": "INT"},
        ])

        column.add("customers", "created_at", "DATETIME2", default="GETDATE()")
        index.add("customers", ["email"], unique=True)
        check.add("customers", "chk_age_positive", "age >= 0")

        print(table.get_definition("customers"))
        print(index.list_by_table("customers"))

        db.disconnect()
    else:
        print("Connection failed:", db.get_last_error())