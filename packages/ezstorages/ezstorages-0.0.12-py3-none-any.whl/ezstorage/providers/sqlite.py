import inspect
from typing import TYPE_CHECKING
from ..tokenizer.types import TokenTypes

if TYPE_CHECKING:    
    from ..table import Table
    from ..tokenizer.token import Token

import sqlite3
from .__template__ import DbProvider

TYPES_SQLITE = {
    int: 'INTEGER',
    str: 'TEXT',
    float: 'REAL',
    bool: 'INTEGER',
}


class Sqlite(DbProvider):
    def __init__(self, path: str):
        self.path = path
        self.name = path.split("/")[-1]
        self.conn = sqlite3.connect(path)
        self.cursor = None

        # Fetch the existing tables
        cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        self.__tables__ = [table[0] for table in cursor.fetchall()]
        
    def _get_schema(self, table: "Table") -> dict:
        """Return the schema of the table"""
        if not table.__exist__:
            return {}
        
        cursor = self.conn.execute(f"PRAGMA table_info({table.__table__})")
        schema = {row[1]: row[2] for row in cursor.fetchall()}
        return schema

    def create_table(self, table: "Table"):
        """Create the table if it does not exist"""
        # Check if the table already exists
        if table.__exist__:
            return

        types = [f"{key} {self._convert_type(value)}" for key, value in table.__annotations__.items()]
        schema = f"CREATE TABLE {table.__table__} ({', '.join(types)})"
        self.conn.execute(schema)
        self.conn.commit()
        table.__exist__ = True
        table.__schema__ = self._get_schema(table)
        self.__tables__.append(table.__table__)

    def drop_table(self, table: "Table"):
        """Drop the table from the database"""
        if not table.__exist__:
            return
        
        self.conn.execute(f"DROP TABLE {table.__table__}")
        self.conn.commit()
        table.__exist__ = False
    
    def update_table(self, table: "Table"):
        """Update the table schema"""
        if not table.__exist__:
            return

        # Add the missing columns
        missing_columns = self._get_missing_columns(table)
        for column in missing_columns:
            column_type = self._convert_type(table.__annotations__[column])
            self.conn.execute(f"ALTER TABLE {table.__table__} ADD COLUMN {column} {column_type}")
            self.conn.commit()

        # Remove the extra columns
        extra_columns = self._get_extra_columns(table)
        for column in extra_columns:
            self.conn.execute(f"ALTER TABLE {table.__table__} DROP COLUMN {column}")
            self.conn.commit()

        # Update the schema
        table.__schema__ = self._get_schema(table)

    def commit(self):
        """Commit the changes to the database"""
        self.conn.commit()
        
    def close(self):
        """Close the connection to the database"""
        self.conn.close()
    ##########################################
    # Database operations
    ##########################################
    def _insert(self, obj: dict, table: str):
        """Insert a row into the table"""
        columns = ', '.join(obj.keys())
        values = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in obj.values()])
        self.conn.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")
        # self.conn.commit()

    def execute(self, query: str):
        """Select the table from the database"""
        if self.cursor:
            self.cursor.execute(query)
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    ##########################################
    # Utility functions
    ##########################################
    def _convert_type(self, type):
        """Convert the type to the sqlite type""" 
        assert type in TYPES_SQLITE, f"Type {type} not supported"
        return TYPES_SQLITE[type]
    
    def _get_missing_columns(self, table: "Table") -> list:
        """Return the missing columns"""
        return [key for key in table.__annotations__ if key not in table.__schema__]
    
    def _get_extra_columns(self, table: "Table") -> list:
        """Return the extra columns"""
        return [key for key in table.__schema__ if key not in table.__annotations__]
    
    def _get_changed_columns(self, table: "Table") -> list:
        """Return the changed columns"""
        return [key for key in table.__annotations__ if key in table.__schema__ and table.__schema__[key] != self._convert_type(table.__annotations__[key])]
    
    def _tokens_to_sql(self, tokens: list["Token"], table: "Table") -> str:
        """Convert the token to a sql string"""
        # Get the table order of elements
        columns = list(table.__annotations__.keys())
        query = "SELECT"
        for column in columns:
            query += " %s," % column
        query = query[:-1] + " FROM %s" % table.__table__

        if not tokens:
            return query
        else:
            query += " WHERE"

        for token in tokens:
            query += " "
            print(token)
            if inspect.isclass(token.token_type):
                query += "%s" % token.value
                continue
            
            match token.token_type:
                case TokenTypes.AND:
                    query += "AND"
                case TokenTypes.OR:
                    query += "OR"
                case TokenTypes.OPEN_PARENTHESIS:
                    query += "("
                case TokenTypes.CLOSE_PARENTHESIS:
                    query += ")"
                case TokenTypes.LESS_THAN:
                    query += "<"
                case TokenTypes.GREATER_THAN:
                    query += ">"
                case TokenTypes.LESS_THAN_EQUAL:
                    query += "<="
                case TokenTypes.GREATER_THAN_EQUAL:
                    query += ">="
                case TokenTypes.EQUAL:
                    query += "="
                case TokenTypes.NOT_EQUAL:
                    query += "!="
                case TokenTypes.IN:
                    query += "IN"
                case TokenTypes.NOT_IN:
                    query += "NOT IN"
                case TokenTypes.CONSTANT:
                    query += "'%s'" % token.value
                
                case Token:
                    query += f" {token.value}"

        return query

    ##########################################
    # Magic methods
    ##########################################
    def __del__(self):
        self.close()

    def __enter__(self):
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            # If there was an exception, rollback any changes
            self.conn.rollback()
        else:
            # Otherwise, commit the changes
            self.conn.commit()

        if self.cursor:
            self.cursor.close()