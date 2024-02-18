from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .providers.__template__ import DbProvider


class Table:
    __exist__: bool = False # If the table exists
    __table__: str = None # The table name
    __schema__: dict = {} # Key value pairs of the schema
    __provider__: "DbProvider" = None # The provider

    def __init__(self, **kwargs):
        # Check if the table name is set
        assert self.__table__ is not None, "Table name not set, create a connector and use the useTable decorator"

        # Assign the values to the object
        for key, value in kwargs.items():
            assert key in self.__annotations__, f"Key {key} not in table {self.__table__}"
            assert isinstance(value, self.__annotations__[key]), f"Value {value} is not of type {self.__annotations__[key]}"
            setattr(self, key, value)

        # Check if all the keys are set
        for key in self.__annotations__:
            assert hasattr(self, key), f"Key {key} not set for table {self.__table__}"
