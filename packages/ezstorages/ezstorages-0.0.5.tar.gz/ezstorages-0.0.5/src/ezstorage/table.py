from .providers.__template__ import DbProvider


class Table:
    __exist__ = False
    __table__ = None
    __provider__: DbProvider = None
    
    def __init__(self):
        assert self.__table__ is not None, "Table name not set, use @useTable decorator"

    @classmethod
    def create_table(cls):
        cls.__provider__.create_table(cls.__table__)
    
    @classmethod
    def drop_table(cls):
        cls.__provider__.drop_table(cls.__table__)

    @classmethod
    def update_table(cls):
        cls.__provider__.update_table(cls.__table__)
