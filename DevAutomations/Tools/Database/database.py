"""
database.py

Interface skeleton (abstract classes) for abstracting DBMS operations
(Database Management System) independent of the underlying database
(PostgreSQL, MySQL, SQL Server, Oracle, SQLite, etc).

Each concrete DBMS should implement these interfaces (e.g. PostgresIndex,
MySQLIndex, PostgresTable, MySQLTable, etc), allowing the database backend
to be swapped without changing the code that consumes these classes.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Common base for schema objects (Index, Check, Column, Table)
# ---------------------------------------------------------------------------
class SchemaObject(ABC):
    """
    Abstract base class for database schema objects (indexes, constraints,
    columns, tables). Defines the minimum contract that every schema object
    must implement.
    """

    @abstractmethod
    def add(self, *args, **kwargs) -> bool:
        """Creates/adds the object in the database."""
        raise NotImplementedError

    @abstractmethod
    def drop(self, *args, **kwargs) -> bool:
        """Permanently removes the object's definition from the database (DDL)."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs) -> bool:
        """
        Removes data associated with the object (DML), as opposed to `drop`,
        which removes the object's definition/structure.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs) -> bool:
        """Updates the object's definition/structure."""
        raise NotImplementedError

    @abstractmethod
    def exists(self, *args, **kwargs) -> bool:
        """Checks whether the object exists in the database."""
        raise NotImplementedError

    # --- Suggested extra methods useful for any SchemaObject ---
    @abstractmethod
    def rename(self, new_name: str) -> bool:
        """Renames the object."""
        raise NotImplementedError

    @abstractmethod
    def get_definition(self) -> str:
        """Returns the object's current DDL/definition (useful for diffs and auditing)."""
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------
class Index(SchemaObject):
    """Interface for index operations."""

    @abstractmethod
    def add(
        self,
        table: str,
        columns: List[str],
        unique: bool = False,
        index_type: Optional[str] = None,
        **kwargs,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def drop(self, table: str, index_name: str, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, table: str, index_name: str, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, table: str, index_name: str, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def exists(self, table: str, index_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def rename(self, new_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_definition(self) -> str:
        raise NotImplementedError

    # --- Index-specific suggestions ---
    @abstractmethod
    def rebuild(self, table: str, index_name: str) -> bool:
        """Rebuilds (REINDEX) a fragmented index."""
        raise NotImplementedError

    @abstractmethod
    def get_usage_stats(self, table: str, index_name: str) -> Dict[str, Any]:
        """Returns usage statistics for the index (scans, size, fragmentation)."""
        raise NotImplementedError

    @abstractmethod
    def list_by_table(self, table: str) -> List[str]:
        """Lists all indexes of a table."""
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Check (check constraints)
# ---------------------------------------------------------------------------
class Check(SchemaObject):
    """Interface for CHECK constraint operations."""

    @abstractmethod
    def add(self, table: str, constraint_name: str, expression: str, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def drop(self, table: str, constraint_name: str, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, table: str, constraint_name: str, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, table: str, constraint_name: str, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def exists(self, table: str, constraint_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def rename(self, new_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_definition(self) -> str:
        raise NotImplementedError

    # --- Check-specific suggestions ---
    @abstractmethod
    def enable(self, table: str, constraint_name: str) -> bool:
        """Enables the constraint (allows validation on new changes)."""
        raise NotImplementedError

    @abstractmethod
    def disable(self, table: str, constraint_name: str) -> bool:
        """Temporarily disables the constraint (e.g. for bulk loads)."""
        raise NotImplementedError

    @abstractmethod
    def validate(self, table: str, constraint_name: str) -> bool:
        """Validates existing data against the constraint, returning whether it passes."""
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Column
# ---------------------------------------------------------------------------
class Column(SchemaObject):
    """Interface for column operations on a table."""

    @abstractmethod
    def add(
        self,
        table: str,
        column_name: str,
        data_type: str,
        nullable: bool = True,
        default: Optional[Any] = None,
        **kwargs,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def drop(self, table: str, column_name: str, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, table: str, column_name: str, **kwargs) -> bool:
        """Clears/removes the column's values without dropping its definition."""
        raise NotImplementedError

    @abstractmethod
    def update(self, table: str, column_name: str, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def exists(self, table: str, column_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def rename(self, new_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_definition(self) -> str:
        raise NotImplementedError

    # --- Column-specific suggestions ---
    @abstractmethod
    def change_type(self, table: str, column_name: str, new_type: str) -> bool:
        """Changes the column's data type (ALTER COLUMN ... TYPE)."""
        raise NotImplementedError

    @abstractmethod
    def set_default(self, table: str, column_name: str, default: Any) -> bool:
        """Sets/changes the column's default value."""
        raise NotImplementedError

    @abstractmethod
    def set_nullable(self, table: str, column_name: str, nullable: bool) -> bool:
        """Sets whether the column accepts NULL."""
        raise NotImplementedError

    @abstractmethod
    def list_by_table(self, table: str) -> List[Dict[str, Any]]:
        """Lists a table's columns with metadata (type, nullability, default)."""
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------------
class Table(SchemaObject):
    """Interface for table operations."""

    @abstractmethod
    def add(self, table_name: str, columns: List[Dict[str, Any]], **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def drop(self, table_name: str, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, table_name: str, where: Optional[str] = None, **kwargs) -> bool:
        """Removes records from the table (DELETE FROM), optionally filtered."""
        raise NotImplementedError

    @abstractmethod
    def update(self, table_name: str, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def exists(self, table_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def rename(self, new_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_definition(self) -> str:
        raise NotImplementedError

    # --- Table-specific suggestions ---
    @abstractmethod
    def truncate(self, table_name: str) -> bool:
        """Removes all records quickly, without row-by-row logging."""
        raise NotImplementedError

    @abstractmethod
    def count_rows(self, table_name: str, where: Optional[str] = None) -> int:
        """Returns the number of records in the table."""
        raise NotImplementedError

    @abstractmethod
    def get_primary_key(self, table_name: str) -> List[str]:
        """Returns the columns that make up the primary key."""
        raise NotImplementedError

    @abstractmethod
    def get_foreign_keys(self, table_name: str) -> List[Dict[str, Any]]:
        """Returns the table's foreign keys."""
        raise NotImplementedError

    @abstractmethod
    def list_tables(self, schema: Optional[str] = None) -> List[str]:
        """Lists existing tables in the database (or in a specific schema)."""
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
class Database(ABC):
    """
    Interface for database-level operations (connection, command/query
    execution, backup and restore).
    """

    @abstractmethod
    def restore(self, backup_path: str, **kwargs) -> bool:
        """Restores the database from a backup file."""
        raise NotImplementedError

    @abstractmethod
    def drop(self, database_name: str, **kwargs) -> bool:
        """Completely removes (drops) the database."""
        raise NotImplementedError

    @abstractmethod
    def execute_sql(self, sql: str, params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Executes a SQL command that does not return tabular results
        (INSERT, UPDATE, DELETE, DDL in general). Returns success/failure.
        """
        raise NotImplementedError

    @abstractmethod
    def execute_query(
        self, sql: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes a SQL query that returns tabular results (SELECT)
        and returns the resulting records.
        """
        raise NotImplementedError

    # --- Suggested extra methods for Database ---
    @abstractmethod
    def connect(self, **kwargs) -> bool:
        """Opens the connection to the database."""
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> bool:
        """Closes the connection to the database."""
        raise NotImplementedError

    @abstractmethod
    def is_connected(self) -> bool:
        """Checks whether the connection to the database is active."""
        raise NotImplementedError

    @abstractmethod
    def create(self, database_name: str, **kwargs) -> bool:
        """Creates a new database."""
        raise NotImplementedError

    @abstractmethod
    def exists(self, database_name: str) -> bool:
        """Checks whether a database exists."""
        raise NotImplementedError

    @abstractmethod
    def backup(self, destination_path: str, **kwargs) -> bool:
        """Generates a backup of the database at the given path."""
        raise NotImplementedError

    @abstractmethod
    def begin_transaction(self) -> bool:
        """Starts an explicit transaction."""
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> bool:
        """Commits the current transaction."""
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> bool:
        """Rolls back the current transaction."""
        raise NotImplementedError

    @abstractmethod
    def get_version(self) -> str:
        """Returns the DBMS version in use."""
        raise NotImplementedError

    @abstractmethod
    def get_last_error(self) -> Optional[str]:
        """Returns the last error message, if any."""
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> bool:
        """Quickly checks whether the database is healthy and responding."""
        raise NotImplementedError
