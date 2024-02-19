```python
from ezstorge import Sqlite, Table, key

db = Sqlite("example.db")
@db.useTable("example")
class TExampleStr(Table):
    id : key.str
    string : str = None # Optional
    integer : int # required
    number : float
    boolean : bool
    date : datetime


@db.useTable("example")
class TExampleAuto(Table):
    id : key.auto
    string : str
    integer : int
    number : float
    boolean : bool
    date : datetime




# Create a single or all tables
db.createTable(TExampleStr)
db.createTables()

# Insert a single or all tables
db.updateTable(TExampleStr)
db.updateTables()

# Delete a single or all tables
db.deleteTable(TExampleStr)
db.deleteTables()


# Allow to have multiple databases
db2 = Sqlite("example2.db")

TExampleStr.select().where(TExampleStr.string == "Hello").execute()



```

import dis

class IterableCar(type):
def **iter**(cls) -> Iterator["Car"]:
return iter([])

class Car(metaclass=IterableCar):
name: str
id: int
