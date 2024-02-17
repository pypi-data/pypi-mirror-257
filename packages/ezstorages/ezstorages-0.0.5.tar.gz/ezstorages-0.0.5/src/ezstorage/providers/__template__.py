from abc import ABC, abstractmethod

# Abstract class for the provider

class DbProvider(ABC):
    @abstractmethod
    def create_table(self):
        """Create the table in the database"""

    @abstractmethod
    def drop_table(self):
        """Drop the table from the database"""

    @abstractmethod
    def update_table(self):
        """Update the table schema in the database"""