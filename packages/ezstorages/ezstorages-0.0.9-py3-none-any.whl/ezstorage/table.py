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

    def to_dict(self):
        """Return the object as a dictionary"""
        return {key: getattr(self, key) for key in self.__annotations__}
    
    def save(self):
        """Save the object to the database"""
        assert self.__exist__, f"Table {self.__table__} does not exist, create it first using the create_table method"  
        self.__provider__._insert(self.to_dict(), self.__table__)

    ##########################################
    # Magic method
    ##########################################
    def __repr__(self):
        content = ', '.join([f'{key}={getattr(self, key)}' for key in self.__annotations__]) 
        return f"{self.__class__.__name__}({content})"
    
    def __iter__(self):
        """Iterate over the values"""
        obj = self.to_dict()
        return iter(obj.items())

    def __getitem__(self, key):
        """Get the value of the key"""
        assert key in self.__annotations__, f"Key {key} not in table {self.__table__}"
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        """Set the value of the key"""
        assert key in self.__annotations__, f"Key {key} not in table {self.__table__}"
        assert isinstance(value, self.__annotations__[key]), f"Value {value} is not of type {self.__annotations__[key]}"
        setattr(self, key, value)

    def __len__(self):
        """Return the number of columns"""
        return len(self.__annotations__)
    
    def __contains__(self, key):
        """Check if the key is in the table"""
        return key in self.__annotations__
    
    def __eq__(self, other):
        """Check if the two objects are equal"""
        return all([getattr(self, key) == getattr(other, key) for key in self.__annotations__])