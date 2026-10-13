"""
postgres_database.py

PostgreSQL implementation of the interfaces defined in database.py
(Database, Index, Check, Column, Table), using psycopg (v3).

Requirements:
    pip install "psycopg[binary]"
    pg_dump / pg_restore available on PATH (used by Database.backup / restore)

Note on the `rename` / `get_definition` signatures:
The base interface (database.py) defines these as stateless, single-argument
methods (`rename(self, new_name)`, `get_definition(self)`), which implies
each instance represents one specific object. This implementation instead
follows a "manager" style (like `add`, `drop`, `exists`, etc.), where a
single Index/Check/Column/Table instance can operate on any object by name.
For that reason, `rename` and `get_definition` below accept the identifying
parameters (table, current name) explicitly. This is a deliberate,
documented deviation from the base signatures to keep the manager-style API
consistent across all methods.
"""

import subprocess
from typing import Any, Dict, List, Optional

import psycopg
from psycopg import sql
from psycopg.rows import dict_row

from database import Check, Column, Database, Index, Table


# ---------------------------------------------------------------------------
# PostgresDatabase
# ---------------------------------------------------------------------------
class PostgresDatabase(Database):
    """PostgreSQL implementation of the Database interface (psycopg 3)."""

    def __init__(self, host: str, port: int = 5432, user: str = "postgres",
                 password: str = "", dbname: str = "postgres"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.conn: Optional[psycopg.Connection] = None
        self._last_error: Optional[str] = None

    # --- connection lifecycle ---
    def connect(self, **kwargs) -> bool:
        try:
            self.conn = psycopg.connect(
                host=self.host, port=self.port, user=self.user,
                password=self.password, dbname=self.dbname,
                autocommit=True, **kwargs,
            )
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
        return self.conn is not None and not self.conn.closed

    # --- database-level operations ---
    def create(self, database_name: str, **kwargs) -> bool:
        try:
            with self._maintenance_connection() as conn:
                conn.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name))
                )
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def drop(self, database_name: str, **kwargs) -> bool:
        try:
            with self._maintenance_connection() as conn:
                conn.execute(
                    sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(database_name))
                )
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def exists(self, database_name: str) -> bool:
        try:
            with self._maintenance_connection() as conn:
                cur = conn.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %(name)s",
                    {"name": database_name},
                )
                return cur.fetchone() is not None
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def _maintenance_connection(self) -> psycopg.Connection:
        """Opens a short-lived autocommit connection to the 'postgres' database
        (CREATE DATABASE / DROP DATABASE cannot run inside a transaction
        block, and can't run against the database being dropped)."""
        return psycopg.connect(
            host=self.host, port=self.port, user=self.user,
            password=self.password, dbname="postgres", autocommit=True,
        )

    # --- backup / restore (delegated to pg_dump / pg_restore CLI tools) ---
    def backup(self, destination_path: str, **kwargs) -> bool:
        try:
            cmd = [
                "pg_dump", "-h", self.host, "-p", str(self.port),
                "-U", self.user, "-F", "c", "-f", destination_path, self.dbname,
            ]
            result = subprocess.run(
                cmd, env={"PGPASSWORD": self.password}, capture_output=True, text=True,
            )
            if result.returncode != 0:
                self._last_error = result.stderr
                return False
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    def restore(self, backup_path: str, **kwargs) -> bool:
        try:
            cmd = [
                "pg_restore", "-h", self.host, "-p", str(self.port),
                "-U", self.user, "-d", self.dbname,
                "--clean", "--if-exists", backup_path,
            ]
            result = subprocess.run(
                cmd, env={"PGPASSWORD": self.password}, capture_output=True, text=True,
            )
            if result.returncode != 0:
                self._last_error = result.stderr
                return False
            return True
        except Exception as exc:
            self._last_error = str(exc)
            return False

    # --- raw SQL execution ---
    def execute_sql(self, sql: str, params: Optional[Dict[str, Any]] = None) -> bool:
        try:
            self.conn.execute(sql, params or {})
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
            with self.conn.cursor(row_factory=dict_row) as cur:
                cur.execute(sql, params or {})
                return list(cur.fetchall())
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
        cur = self.conn.execute("SELECT version()")
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
# PostgresIndex
# ---------------------------------------------------------------------------
class PostgresIndex(Index):
    """PostgreSQL implementation of the Index interface."""

    def __init__(self, database: PostgresDatabase):
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
            concurrently = sql.SQL("CONCURRENTLY ") if kwargs.get("concurrently") else sql.SQL("")
            unique_kw = sql.SQL("UNIQUE ") if unique else sql.SQL("")
            using_kw = (
                sql.SQL("USING {} ").format(sql.Identifier(index_type)) if index_type else sql.SQL("")
            )
            query = sql.SQL(
                "CREATE {unique}INDEX {concurrently}{name} ON {table} {using}({cols})"
            ).format(
                unique=unique_kw,
                concurrently=concurrently,
                name=sql.Identifier(index_name),
                table=sql.Identifier(table),
                using=using_kw,
                cols=sql.SQL(", ").join(map(sql.Identifier, columns)),
            )
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def drop(self, table: str, index_name: str, **kwargs) -> bool:
        try:
            self.db.conn.execute(
                sql.SQL("DROP INDEX IF EXISTS {}").format(sql.Identifier(index_name))
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
        # Postgres has no ALTER INDEX to change columns/uniqueness; the
        # index must be dropped and recreated with the new definition.
        if not self.drop(table, index_name):
            return False
        columns = kwargs.pop("columns", [])
        unique = kwargs.pop("unique", False)
        index_type = kwargs.pop("index_type", None)
        kwargs["index_name"] = index_name
        return self.add(table, columns, unique=unique, index_type=index_type, **kwargs)

    def exists(self, table: str, index_name: str) -> bool:
        rows = self.db.execute_query(
            "SELECT 1 FROM pg_indexes WHERE tablename = %(table)s AND indexname = %(index_name)s",
            {"table": table, "index_name": index_name},
        )
        return len(rows) > 0

    def rename(self, table: str, old_name: str, new_name: str) -> bool:
        try:
            self.db.conn.execute(
                sql.SQL("ALTER INDEX {} RENAME TO {}").format(
                    sql.Identifier(old_name), sql.Identifier(new_name)
                )
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_definition(self, table: str, index_name: str) -> str:
        rows = self.db.execute_query(
            "SELECT indexdef FROM pg_indexes WHERE tablename = %(table)s AND indexname = %(index_name)s",
            {"table": table, "index_name": index_name},
        )
        return rows[0]["indexdef"] if rows else ""

    # --- index-specific extras ---
    def rebuild(self, table: str, index_name: str) -> bool:
        try:
            self.db.conn.execute(sql.SQL("REINDEX INDEX {}").format(sql.Identifier(index_name)))
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_usage_stats(self, table: str, index_name: str) -> Dict[str, Any]:
        rows = self.db.execute_query(
            """
            SELECT idx_scan, idx_tup_read, idx_tup_fetch,
                   pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
            FROM pg_stat_user_indexes
            WHERE relname = %(table)s AND indexrelname = %(index_name)s
            """,
            {"table": table, "index_name": index_name},
        )
        return rows[0] if rows else {}

    def list_by_table(self, table: str) -> List[str]:
        rows = self.db.execute_query(
            "SELECT indexname FROM pg_indexes WHERE tablename = %(table)s",
            {"table": table},
        )
        return [row["indexname"] for row in rows]


# ---------------------------------------------------------------------------
# PostgresCheck
# ---------------------------------------------------------------------------
class PostgresCheck(Check):
    """PostgreSQL implementation of the Check interface (CHECK constraints)."""

    def __init__(self, database: PostgresDatabase):
        self.db = database

    def add(self, table: str, constraint_name: str, expression: str, **kwargs) -> bool:
        try:
            not_valid = sql.SQL(" NOT VALID") if kwargs.get("not_valid") else sql.SQL("")
            query = sql.SQL("ALTER TABLE {table} ADD CONSTRAINT {name} CHECK ({expr}){not_valid}").format(
                table=sql.Identifier(table),
                name=sql.Identifier(constraint_name),
                expr=sql.SQL(expression),  # expression is raw SQL, not a value -> cannot be a bind param
                not_valid=not_valid,
            )
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def drop(self, table: str, constraint_name: str, **kwargs) -> bool:
        try:
            self.db.conn.execute(
                sql.SQL("ALTER TABLE {table} DROP CONSTRAINT IF EXISTS {name}").format(
                    table=sql.Identifier(table), name=sql.Identifier(constraint_name)
                )
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def delete(self, table: str, constraint_name: str, **kwargs) -> bool:
        # A CHECK constraint has no data of its own; deleting == dropping it.
        return self.drop(table, constraint_name, **kwargs)

    def update(self, table: str, constraint_name: str, **kwargs) -> bool:
        # Postgres has no ALTER CONSTRAINT to change a CHECK expression;
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
            SELECT 1 FROM pg_constraint c
            JOIN pg_class t ON t.oid = c.conrelid
            WHERE t.relname = %(table)s AND c.conname = %(name)s AND c.contype = 'c'
            """,
            {"table": table, "name": constraint_name},
        )
        return len(rows) > 0

    def rename(self, table: str, old_name: str, new_name: str) -> bool:
        try:
            self.db.conn.execute(
                sql.SQL("ALTER TABLE {table} RENAME CONSTRAINT {old} TO {new}").format(
                    table=sql.Identifier(table),
                    old=sql.Identifier(old_name),
                    new=sql.Identifier(new_name),
                )
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_definition(self, table: str, constraint_name: str) -> str:
        rows = self.db.execute_query(
            """
            SELECT pg_get_constraintdef(c.oid) AS definition
            FROM pg_constraint c
            JOIN pg_class t ON t.oid = c.conrelid
            WHERE t.relname = %(table)s AND c.conname = %(name)s
            """,
            {"table": table, "name": constraint_name},
        )
        return rows[0]["definition"] if rows else ""

    # --- check-specific extras ---
    def enable(self, table: str, constraint_name: str) -> bool:
        # Postgres has no native "enable" for CHECK constraints; the closest
        # equivalent is marking a NOT VALID constraint as validated.
        return self.validate(table, constraint_name)

    def disable(self, table: str, constraint_name: str) -> bool:
        # Postgres has no native way to disable a CHECK constraint without
        # dropping it (unlike Oracle/SQL Server). Documented limitation.
        self.db._last_error = (
            "PostgreSQL does not support disabling CHECK constraints; drop() is the only option"
        )
        return False

    def validate(self, table: str, constraint_name: str) -> bool:
        try:
            self.db.conn.execute(
                sql.SQL("ALTER TABLE {table} VALIDATE CONSTRAINT {name}").format(
                    table=sql.Identifier(table), name=sql.Identifier(constraint_name)
                )
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False


# ---------------------------------------------------------------------------
# PostgresColumn
# ---------------------------------------------------------------------------
class PostgresColumn(Column):
    """PostgreSQL implementation of the Column interface."""

    def __init__(self, database: PostgresDatabase):
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
            not_null = sql.SQL("") if nullable else sql.SQL(" NOT NULL")
            default_clause = sql.SQL("")
            if default is not None:
                default_clause = sql.SQL(" DEFAULT {}").format(sql.Literal(default))
            query = sql.SQL("ALTER TABLE {table} ADD COLUMN {col} {type}{default}{not_null}").format(
                table=sql.Identifier(table),
                col=sql.Identifier(column_name),
                type=sql.SQL(data_type),
                default=default_clause,
                not_null=not_null,
            )
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def drop(self, table: str, column_name: str, **kwargs) -> bool:
        try:
            self.db.conn.execute(
                sql.SQL("ALTER TABLE {table} DROP COLUMN IF EXISTS {col}").format(
                    table=sql.Identifier(table), col=sql.Identifier(column_name)
                )
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def delete(self, table: str, column_name: str, **kwargs) -> bool:
        """Clears the column's values (sets them to NULL) without dropping it."""
        try:
            self.db.conn.execute(
                sql.SQL("UPDATE {table} SET {col} = NULL").format(
                    table=sql.Identifier(table), col=sql.Identifier(column_name)
                )
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
            SELECT 1 FROM information_schema.columns
            WHERE table_name = %(table)s AND column_name = %(col)s
            """,
            {"table": table, "col": column_name},
        )
        return len(rows) > 0

    def rename(self, table: str, old_name: str, new_name: str) -> bool:
        try:
            self.db.conn.execute(
                sql.SQL("ALTER TABLE {table} RENAME COLUMN {old} TO {new}").format(
                    table=sql.Identifier(table),
                    old=sql.Identifier(old_name),
                    new=sql.Identifier(new_name),
                )
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_definition(self, table: str, column_name: str) -> str:
        rows = self.db.execute_query(
            """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = %(table)s AND column_name = %(col)s
            """,
            {"table": table, "col": column_name},
        )
        if not rows:
            return ""
        row = rows[0]
        nullable = "" if row["is_nullable"] == "YES" else " NOT NULL"
        default = f" DEFAULT {row['column_default']}" if row["column_default"] else ""
        return f"{row['column_name']} {row['data_type']}{default}{nullable}"

    # --- column-specific extras ---
    def change_type(self, table: str, column_name: str, new_type: str) -> bool:
        try:
            query = sql.SQL(
                "ALTER TABLE {table} ALTER COLUMN {col} TYPE {type} USING {col}::{type}"
            ).format(
                table=sql.Identifier(table),
                col=sql.Identifier(column_name),
                type=sql.SQL(new_type),
            )
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def set_default(self, table: str, column_name: str, default: Any) -> bool:
        try:
            if default is None:
                query = sql.SQL("ALTER TABLE {table} ALTER COLUMN {col} DROP DEFAULT").format(
                    table=sql.Identifier(table), col=sql.Identifier(column_name)
                )
            else:
                query = sql.SQL("ALTER TABLE {table} ALTER COLUMN {col} SET DEFAULT {value}").format(
                    table=sql.Identifier(table),
                    col=sql.Identifier(column_name),
                    value=sql.Literal(default),
                )
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def set_nullable(self, table: str, column_name: str, nullable: bool) -> bool:
        try:
            action = sql.SQL("DROP NOT NULL") if nullable else sql.SQL("SET NOT NULL")
            query = sql.SQL("ALTER TABLE {table} ALTER COLUMN {col} {action}").format(
                table=sql.Identifier(table), col=sql.Identifier(column_name), action=action
            )
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def list_by_table(self, table: str) -> List[Dict[str, Any]]:
        return self.db.execute_query(
            """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = %(table)s
            ORDER BY ordinal_position
            """,
            {"table": table},
        )


# ---------------------------------------------------------------------------
# PostgresTable
# ---------------------------------------------------------------------------
class PostgresTable(Table):
    """PostgreSQL implementation of the Table interface."""

    def __init__(self, database: PostgresDatabase):
        self.db = database

    def add(self, table_name: str, columns: List[Dict[str, Any]], **kwargs) -> bool:
        """
        columns: list of dicts, e.g.
            [{"name": "id", "type": "SERIAL", "primary_key": True},
             {"name": "email", "type": "TEXT", "nullable": False}]
        """
        try:
            column_defs = []
            pk_columns = []
            for col in columns:
                parts = [sql.Identifier(col["name"]), sql.SQL(col["type"])]
                if not col.get("nullable", True):
                    parts.append(sql.SQL("NOT NULL"))
                if col.get("default") is not None:
                    parts.append(sql.SQL("DEFAULT {}").format(sql.Literal(col["default"])))
                column_defs.append(sql.SQL(" ").join(parts))
                if col.get("primary_key"):
                    pk_columns.append(col["name"])

            if pk_columns:
                column_defs.append(
                    sql.SQL("PRIMARY KEY ({})").format(
                        sql.SQL(", ").join(map(sql.Identifier, pk_columns))
                    )
                )

            query = sql.SQL("CREATE TABLE {table} ({defs})").format(
                table=sql.Identifier(table_name),
                defs=sql.SQL(", ").join(column_defs),
            )
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def drop(self, table_name: str, **kwargs) -> bool:
        try:
            cascade = sql.SQL(" CASCADE") if kwargs.get("cascade") else sql.SQL("")
            self.db.conn.execute(
                sql.SQL("DROP TABLE IF EXISTS {table}{cascade}").format(
                    table=sql.Identifier(table_name), cascade=cascade
                )
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def delete(self, table_name: str, where: Optional[str] = None, **kwargs) -> bool:
        try:
            where_clause = sql.SQL(" WHERE {}").format(sql.SQL(where)) if where else sql.SQL("")
            self.db.conn.execute(
                sql.SQL("DELETE FROM {table}{where}").format(
                    table=sql.Identifier(table_name), where=where_clause
                )
            )
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

            set_parts = [
                sql.SQL("{} = {}").format(sql.Identifier(col), sql.Literal(val))
                for col, val in values.items()
            ]
            where_clause = sql.SQL(" WHERE {}").format(sql.SQL(where)) if where else sql.SQL("")

            query = sql.SQL("UPDATE {table} SET {sets}{where}").format(
                table=sql.Identifier(table_name),
                sets=sql.SQL(", ").join(set_parts),
                where=where_clause,
            )
            self.db.conn.execute(query)
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def exists(self, table_name: str) -> bool:
        rows = self.db.execute_query(
            "SELECT 1 FROM information_schema.tables WHERE table_name = %(name)s",
            {"name": table_name},
        )
        return len(rows) > 0

    def rename(self, table_name: str, new_name: str) -> bool:
        try:
            self.db.conn.execute(
                sql.SQL("ALTER TABLE {table} RENAME TO {new}").format(
                    table=sql.Identifier(table_name), new=sql.Identifier(new_name)
                )
            )
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def get_definition(self, table_name: str) -> str:
        """Builds a simplified CREATE TABLE statement from catalog metadata."""
        columns = self.db.execute_query(
            """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = %(name)s
            ORDER BY ordinal_position
            """,
            {"name": table_name},
        )
        if not columns:
            return ""

        column_lines = []
        for col in columns:
            line = f"{col['column_name']} {col['data_type']}"
            if col["column_default"]:
                line += f" DEFAULT {col['column_default']}"
            if col["is_nullable"] == "NO":
                line += " NOT NULL"
            column_lines.append(line)

        return f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(column_lines) + "\n);"

    # --- table-specific extras ---
    def truncate(self, table_name: str) -> bool:
        try:
            self.db.conn.execute(sql.SQL("TRUNCATE TABLE {}").format(sql.Identifier(table_name)))
            return True
        except Exception as exc:
            self.db._last_error = str(exc)
            return False

    def count_rows(self, table_name: str, where: Optional[str] = None) -> int:
        where_sql = f" WHERE {where}" if where else ""
        rows = self.db.execute_query(f"SELECT COUNT(*) AS total FROM {table_name}{where_sql}")
        return rows[0]["total"] if rows else 0

    def get_primary_key(self, table_name: str) -> List[str]:
        rows = self.db.execute_query(
            """
            SELECT a.attname AS column_name
            FROM pg_index i
            JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
            WHERE i.indrelid = %(table)s::regclass AND i.indisprimary
            """,
            {"table": table_name},
        )
        return [row["column_name"] for row in rows]

    def get_foreign_keys(self, table_name: str) -> List[Dict[str, Any]]:
        return self.db.execute_query(
            """
            SELECT
                tc.constraint_name,
                kcu.column_name,
                ccu.table_name  AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
                ON tc.constraint_name = ccu.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = %(table)s
            """,
            {"table": table_name},
        )

    def list_tables(self, schema: Optional[str] = None) -> List[str]:
        schema = schema or "public"
        rows = self.db.execute_query(
            """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = %(schema)s AND table_type = 'BASE TABLE'
            """,
            {"schema": schema},
        )
        return [row["table_name"] for row in rows]


# ---------------------------------------------------------------------------
# Usage example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    db = PostgresDatabase(host="localhost", port=5432, user="postgres",
                           password="postgres", dbname="my_app")
    if db.connect():
        table = PostgresTable(db)
        column = PostgresColumn(db)
        index = PostgresIndex(db)
        check = PostgresCheck(db)

        table.add("customers", [
            {"name": "id", "type": "SERIAL", "primary_key": True},
            {"name": "name", "type": "TEXT", "nullable": False},
            {"name": "email", "type": "TEXT", "nullable": False},
            {"name": "age", "type": "INTEGER"},
        ])

        column.add("customers", "created_at", "TIMESTAMP", default="now()")
        index.add("customers", ["email"], unique=True)
        check.add("customers", "chk_age_positive", "age >= 0")

        print(table.get_definition("customers"))
        print(index.list_by_table("customers"))

        db.disconnect()
    else:
        print("Connection failed:", db.get_last_error())