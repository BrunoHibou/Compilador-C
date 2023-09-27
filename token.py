from enum import Enum


class TokenClass(Enum):
    NUMERICAL_CONSTANT = 1,
    ID = 2,
    SYMBOL = 3,


class Token:
    def __init__(self, token_class: TokenClass, token_value):
        self.token_class = token_class
        self.token_value = token_value
    def __str__(self) -> str:
        return f'<Token class: {self.token_class}, value: {self.token_value}>'
