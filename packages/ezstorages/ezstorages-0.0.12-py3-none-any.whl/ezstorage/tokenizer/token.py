import inspect
from .types import TokenTypes


class Token:
    CHAIN = ["and", "or"]
    COMPARISON = ["<", ">", "<=", ">=", "==", "!=", "in", "not in"]
    PARENTHESES = ["(", ")"]

    def __init__(self, value: str, token_type: str):
        # A token can be a Table child class or a token type
        self.value = value
        self.token_type = token_type

    @classmethod
    def from_chain(cls, value: str) -> "Token":
        """Create a token from a chain operator"""
        match value:
            case "and":
                return cls(value, TokenTypes.AND)
            case "or":
                return cls(value, TokenTypes.OR)
            case _:
                raise ValueError(f"Invalid chain operator: {value}")

    @classmethod
    def from_comparison(cls, value: str) -> "Token":
        """Create a token from a comparison operator"""
        match value:
            case "<":
                return cls(value, TokenTypes.LESS_THAN)
            case ">":
                return cls(value, TokenTypes.GREATER_THAN)
            case "<=":
                return cls(value, TokenTypes.LESS_THAN_EQUAL)
            case ">=":
                return cls(value, TokenTypes.GREATER_THAN_EQUAL)
            case "==":
                return cls(value, TokenTypes.EQUAL)
            case "!=":
                return cls(value, TokenTypes.NOT_EQUAL)
            case "in":
                return cls(value, TokenTypes.IN)
            case "not in":
                return cls(value, TokenTypes.NOT_IN)
            case _:
                raise ValueError(f"Invalid comparison operator: {value}")
        
    @classmethod
    def from_parentheses(cls, value: str) -> "Token":
        """Create a token from a parentheses"""
        match value:
            case "(":
                return cls(value, TokenTypes.OPEN_PARENTHESIS)
            case ")":
                return cls(value, TokenTypes.CLOSE_PARENTHESIS)
            case _:
                raise ValueError(f"Invalid parentheses: {value}")

    ##################################################
    # Magic methods
    ##################################################
    def __repr__(self):
        # Check if the token is a Table child
        if inspect.isclass(self.token_type):
            return f"{self.token_type.__name__}('{self.value}')"
        
        return f"{self.token_type.capitalize()}('{self.value}')"
  
        
    def __eq__(self, other: "Token"):
        return self.value == other.value and self.token_type == other.token_type