from .table import Table
from .providers import SqliteProvider


def defineStorage(name: str, provider: str):
    """Decorator to define the storage provider for a table""" 
    def decorator(cls: Table):
        cls.__table__ = name
        return cls
    return decorator
