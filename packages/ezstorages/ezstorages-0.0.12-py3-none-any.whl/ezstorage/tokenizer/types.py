class TokenTypes:
    """A class to hold the various token types"""
    # Chain operators
    AND = "AND" # and
    OR = "OR" # or

    # Comparison operators
    EQUAL = "EQUAL" # ==
    NOT_EQUAL = "NOT_EQUAL" # !=
    LESS_THAN = "LESS_THAN" # <
    GREATER_THAN = "GREATER_THAN" # >
    LESS_THAN_EQUAL = "LESS_THAN_EQUAL" # <=
    GREATER_THAN_EQUAL = "GREATER_THAN_EQUAL" # >=
    IN = "IN" # in
    NOT_IN = "NOT_IN" # not in

    # Variables
    VARIABLE = "VARIABLE" # variable or function
    CONSTANT = "CONSTANT" # number or string
    TABLE = "TABLE" # table

    # Parentheses
    OPEN_PARENTHESIS = "OPEN_PARENTHESIS" # (
    CLOSE_PARENTHESIS = "CLOSE_PARENTHESIS" # )