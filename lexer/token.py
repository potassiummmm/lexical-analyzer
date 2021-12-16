from enum import Enum


class TokenType(Enum):
    KEYWORD = 'K'
    IDENTIFIER = 'V'
    INTEGER = 'I'
    OPERATOR = 'O'
    DELIMITER = 'D'


class Token:
    reserved_word = {
        'PROGRAM': TokenType.KEYWORD,
        'BEGIN': TokenType.KEYWORD,
        'END': TokenType.KEYWORD,
        'CONST': TokenType.KEYWORD,
        'VAR': TokenType.KEYWORD,
        'WHILE': TokenType.KEYWORD,
        'DO': TokenType.KEYWORD,
        'IF': TokenType.KEYWORD,
        'THEN': TokenType.KEYWORD,
        '+': TokenType.OPERATOR,
        '-': TokenType.OPERATOR,
        '*': TokenType.OPERATOR,
        '/': TokenType.OPERATOR,
        ':=': TokenType.DELIMITER,
        '=': TokenType.DELIMITER,
        '<>': TokenType.DELIMITER,
        '>': TokenType.DELIMITER,
        '>=': TokenType.DELIMITER,
        '<': TokenType.DELIMITER,
        '<=': TokenType.DELIMITER,
        '(': TokenType.DELIMITER,
        ')': TokenType.DELIMITER,
        ';': TokenType.DELIMITER,
        ',': TokenType.DELIMITER,
    }

    def __init__(self):
        self.haha = dict()

    @staticmethod
    def get_token_type(token: str):
        if token in Token.reserved_word:
            return Token.reserved_word[token]
        return TokenType.INTEGER if token[0].isdigit() else TokenType.IDENTIFIER

    @staticmethod
    def print_token(token: str):
        print(f'<{Token.get_token_type(token).value}, {token}>')
