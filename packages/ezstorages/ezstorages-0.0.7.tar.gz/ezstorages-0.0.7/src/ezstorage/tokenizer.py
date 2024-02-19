import re
import inspect
from typing import Callable


class LambdaTokenizer:
    def __init__(self, expression: str | Callable):
        if callable(expression):
            expression = self.clean_lambda(expression)
        self.expression = expression

        # self.pattern = r'(\b\w+\.\w+\b|\b\w+\b(?:\(\))?)|(["\'].*?["\'])|([<>!=]=?|==|in(?: not)?|and|or)|(\d+)|(\[\])|(\[.*?\])|(\(.*?\))|(\s)'
        self.pattern = r'(\b\w+\.\w+\b|\b\w+\b(?:\(\))?)|(["\'].*?["\'])|([<>!=]=?|==|in( not)?|and|or|not in)|(\d+)|(\[\])|(\[.*?\])|(\(.*?\))|(\s)'
        self.pattern = r'(\bnot\s+in\b)|(\b\w+\.\w+\b|\b\w+\b(?:\(\))?)|(["\'].*?["\'])|([<>!=]=?|==|in|and|or)|(\d+)|(\[\])|(\[.*?\])|(\(.*?\))|(\s)'

    @staticmethod
    def clean_lambda(fnx: Callable):
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

    def tokenize(self, expression: str = None):
        """Tokenize the input expression and return a list of tokens"""
        expression = expression or self.expression

        # Regular expression pattern to match various tokens
        tokens = re.findall(self.pattern, expression)
    
        # Check for nested parentheses and flatten the results
        flat_tokens: list[str] = [token for group in tokens for token in group if token.strip()]

        final_tokens = []
        for token in flat_tokens:
            if token.startswith('(') and token.endswith(')'):
                final_tokens += ["(", *self.tokenize(token[1:-1]) ,")"]
            else:
                final_tokens += [token]
    
        return final_tokens
    

