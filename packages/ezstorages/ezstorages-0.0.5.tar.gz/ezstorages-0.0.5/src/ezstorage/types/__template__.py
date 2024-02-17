from datetime import datetime
from abc import ABC, abstractmethod


# Abstract class for the types
class DbTypes(ABC):
    int = "int"
    str = "str"
    bool = "bool"
    float = "float"
    datetime = "datetime"

