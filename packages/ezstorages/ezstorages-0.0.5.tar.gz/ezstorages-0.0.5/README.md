```python
@useTable("example_str")
class TExampleStr(EZsqlite):
    id : key.str
    string : str = None
    integer : int
    number : float
    boolean : bool
    date : datetime


@useTable("example_auto")
class TExampleAuto(EZsqlite):
    id : key.auto
    string : str
    integer : int
    number : float
    boolean : bool
    date : datetime
```
