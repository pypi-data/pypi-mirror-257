import re
import sys
import inspect
from typing import Callable
from .token import Token
from .types import TokenTypes
from ..table import Table


class LambdaTokenizer:
    def __init__(self, expression: str | Callable):
        if callable(expression):
            expression = self.get_expression(expression)
        self.expression = expression
        
        # Create the regular expression pattern to match various tokens
        self.pattern = ""
        self.pattern += r'(\bnot\s+in\b)|' # not in
        self.pattern += r'(\b\w+\.\w+\b|\b\w+\b(?:\(\))?)|' # variable or function
        self.pattern += r'(["\'].*?["\'])|' # string
        self.pattern += r'([<>!=]=?|==|in|and|or)|' # comparison operators
        self.pattern += r'(\d+)|' # number
        self.pattern += r'(\[\])|' # empty list
        self.pattern += r'(\[.*?\])|' # list
        self.pattern += r'(\(.*?\))|' # parentheses
        self.pattern += r'(\s)' # whitespace
        self.pattern = self.pattern.replace("\n", "").replace(" ", "")
       

    @staticmethod
    def get_expression(fnx: Callable) -> str:
        """Extract the lambda expression from the source code"""

        assert callable(fnx) and fnx.__name__ == "<lambda>", "The input must be a lambda expression"
        assert len(inspect.signature(fnx).parameters) == 0, "The lambda expression must not have any arguments"

        # Get the source code of the lambda expression
        source = inspect.getsource(fnx)

        # Extract the lambda expression from the source code
        source = source[source.find("lambda") + len("lambda"):]
        source = source[source.index(":") + 1:]
        source = source.strip()

        # Remove any leading or trailing parentheses
        parentheses = 0
        cleaned_source = ""
        for k in source:
            if k == "(": 
                parentheses += 1

            if k == ")":
                parentheses -= 1

            if k == ")" and parentheses < 0:
                break

            cleaned_source += k
        source = cleaned_source.strip()

        return source

    def get_tokens(self, expression: str = None) -> list[str]:
        """Extract the tokens from the expression"""
        expression = expression or self.expression

        # Regular expression pattern to match various tokens
        tokens = re.findall(self.pattern, expression)
    
        # Check for nested parentheses and flatten the results
        flat_tokens: list[str] = [token for group in tokens for token in group if token.strip()]

        final_tokens = []
        for token in flat_tokens:
            if token.startswith('(') and token.endswith(')'):
                final_tokens += ["(", *self.get_tokens(token[1:-1]) ,")"]
            else:
                final_tokens += [token]
    
        return final_tokens
    
    def tokenize(self):
        """Tokenize the expression"""
        chunks = self.get_tokens()

        tokens = []
        for token in chunks:
            # Check for chain operators
            if token in Token.COMPARISON:
                tokens.append(Token.from_comparison(token))
                continue

            # Check for chain operators
            if token in Token.CHAIN:
                tokens.append(Token.from_chain(token))
                continue
                
            # Check for parentheses
            if token in Token.PARENTHESES:
                tokens.append(Token.from_parentheses(token))
                continue

            # If it's a digit, create a token from it
            if token.isdigit():
                tokens.append(Token(token, TokenTypes.CONSTANT))
                continue
            
            # If it's a string, create a token from it
            if token.startswith('"') or token.startswith("'"):
                tokens.append(Token(token[1:-1], TokenTypes.CONSTANT))
                continue
        

            # Try to load the table class
            if "." in token:  
                elements = token.split(".")  
                try:
                    element = self.run_code_in_frame(elements[0])
                    assert issubclass(element, Table), f"Class {elements[0]} is not a subclass of Table"
                    tokens.append(Token(elements[1], element))
                    continue
                except AssertionError or KeyError:
                    pass
                
            # If it's not a class, try to get the value from the module where was defined
            code = self.run_code_in_frame(token)
            tokens.append(Token(str(code), TokenTypes.CONSTANT))

        return tokens
    
    def run_code_in_frame(self, token: str, max_depth: int = 10):
        """Get the content of a variable"""
        frame = inspect.currentframe().f_back
        string = token.split(".")[0] if "." in token else token

        # Get the module where the lambda expression is defined
        for _ in range(max_depth):
            if string in frame.f_locals:
                break
        
            if string in frame.f_globals:
                break

            frame = frame.f_back
        
        assert string in frame.f_locals or string in frame.f_globals, f"Variable {string} not found in the module"
       
        # Use the module to execute the code
        frame_globals = frame.f_globals
        frame_locals = frame.f_locals

        # Prepare the context to execute the code
        full_code = f'__return_value__ = {token}'

        # Execute the code in the frame context
        exec(full_code, frame_globals, frame_locals)

        # clean up the frame
        return_value = frame_locals['__return_value__']
        del frame_locals['__return_value__']

        return return_value
        


