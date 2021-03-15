"""
If you haven't done so yet, then, as an exercise, re-implement the interpreter in this article
without looking at the source code and use part10.pas as your test input file.
"""

EOF = 'EOF'
INTEGER = 'INTEGER'
REAL = 'REAL'
PLUS = 'PLUS'
MINUS = 'MINUS'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token(' + self.type + ', ' + str(self.value) + ')'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, obj):
        return isinstance(obj, Token) and obj.type == self.type and obj.value == self.value


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def current_char(self):
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def advance(self):
        self.pos += 1

    def skip_whitespace(self):
        while self.current_char() is not None and self.current_char().isspace():
            self.advance()

    def number(self):
        value = ''
        while (self.current_char() is not None and self.current_char().isdigit()):
            value += self.current_char()
            self.advance()
        if (self.current_char() == '.'):
            value += '.'
            self.advance()
            while (self.current_char() is not None and self.current_char().isdigit()):
                value += self.current_char()
                self.advance()
            return Token(REAL, float(value))
        else:
            return Token(INTEGER, int(value))

    def get_next_token(self):
        if (self.current_char() is None):
            return Token(EOF, '')
        if (self.current_char().isspace()):
            self.skip_whitespace()
        if (self.current_char() is None):
            return Token(EOF, '')
        if (self.current_char().isdigit()):
            return self.number()  # method advances sufficiently
        if (self.current_char() == '+'):
            token = Token(PLUS, '+')
            self.advance()
            return token
        if (self.current_char() == '-'):
            token = Token(MINUS, '-')
            self.advance()
            return token
        if (self.current_char() == '('):
            token = Token(LPAREN, '(')
            self.advance()
            return token
        if (self.current_char() == ')'):
            token = Token(RPAREN, ')')
            self.advance()
            return token


def lex(text):
    lexer = Lexer(text)
    tokens = []
    nextToken = lexer.get_next_token()
    while nextToken.type is not EOF:
        tokens.append(nextToken)
        nextToken = lexer.get_next_token()
    return tokens
