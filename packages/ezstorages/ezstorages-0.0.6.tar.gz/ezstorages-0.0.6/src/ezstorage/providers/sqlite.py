from typing import TYPE_CHECKING


if TYPE_CHECKING:    
    from ..table import Table   

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

        # Fetch the existing tables
        cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        self.__tables__ = [table[0] for table in cursor.fetchall()]
        
    def close(self):
        """Close the connection to the database"""
        self.conn.close()

    def get_schema(self, table: "Table") -> dict:
        """Return the schema of the table"""
        if not table.__exist__:
            return False
        
        cursor = self.conn.execute(f"PRAGMA table_info({table.__table__})")
        schema = {row[1]: row[2] for row in cursor.fetchall()}
        return schema

    def create_column(self):
        pass

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
        table.__schema__ = self.get_schema(table)

    def create_tables(self):
        """Create all the tables"""
        for table in self.__classes__:
            self.create_table(table)

    def drop_table(self, table: "Table"):
        """Drop the table from the database"""
        if not table.__exist__:
            return
        
        self.conn.execute(f"DROP TABLE {table.__table__}")
        self.conn.commit()
        table.__exist__ = False
    
    def drop_tables(self):
        """Drop all the tables"""
        for table in self.__classes__:
            self.drop_table(table)

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

    def update_tables(self):
        """Update all the tables"""
        for table in self.__classes__:
            self.update_table(table)

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
    
    ##########################################
    # Magic methods
    ##########################################
    def __del__(self):
        self.close()