"""
If you haven't done so yet, then, as an exercise, re-implement the interpreter in this article
without looking at the source code and use part10.pas as your test input file.
"""

# Token Types
PROGRAM = 'PROGRAM'
SEMI = 'SEMI'
DOT = 'DOT'
VAR = 'VAR'
ID = 'ID'
COMMA = 'COMMA'
COLON = 'COLON'
INTEGER = 'INTEGER'
REAL = 'REAL'
BEGIN = 'BEGIN'
END = 'END'
ASSIGN = 'ASSIGN'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
INTEGER_DIV = 'INTEGER_DIV'
FLOAT_DIV = 'FLOAT_DIV'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST = 'REAL_CONST'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'


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

    def peek(self):
        next_pos = self.pos + 1
        if next_pos >= len(self.text):
            return None
        return self.text[next_pos]

    def error(self):
        raise Exception(
            'An error occurred while lexing the text. Current character: ' + self.current_char())

    def advance(self):
        self.pos += 1

    def skip_whitespace(self):
        while self.current_char() is not None and self.current_char().isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char() != '}':
            if (self.current_char() is None):
                self.error()
            self.advance()
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
            return Token(REAL_CONST, float(value))
        else:
            return Token(INTEGER_CONST, int(value))

    def alpha(self):
        value = ''
        while self.current_char() is not None and (self.current_char().isalpha() or self.current_char().isdigit()):
            value += self.current_char()
            self.advance()
        if (value.upper() == 'PROGRAM'):
            return Token(PROGRAM, value)
        if (value.upper() == 'VAR'):
            return Token(VAR, value)
        if (value.upper() == 'BEGIN'):
            return Token(BEGIN, value)
        if (value.upper() == 'END'):
            return Token(END, value)
        if (value.upper() == 'DIV'):
            return Token(INTEGER_DIV, value)
        if (value.upper() == 'REAL'):
            return Token(REAL, value)
        if (value.upper() == 'INTEGER'):
            return Token(INTEGER, value)
        return Token(ID, value)

    def get_next_token(self):
        if (self.current_char() is not None and self.current_char().isspace()):
            self.skip_whitespace()
        if (self.current_char() == '{'):
            self.skip_comment()
            return self.get_next_token()
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
        if (self.current_char() == '*'):
            token = Token(MUL, '*')
            self.advance()
            return token
        if (self.current_char() == '/'):
            token = Token(FLOAT_DIV, '/')
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
        if (self.current_char() == ';'):
            token = Token(SEMI, ';')
            self.advance()
            return token
        if (self.current_char() == ','):
            token = Token(COMMA, ',')
            self.advance()
            return token
        if (self.current_char() == ':'):
            next_char = self.peek()
            if (next_char is not None and next_char == '='):
                token = Token(ASSIGN, ':=')
                self.advance()
                self.advance()
                return token
            token = Token(COLON, ':')
            self.advance()
            return token
        if (self.current_char() == '.'):
            token = Token(DOT, '.')
            self.advance()
            return token
        if (self.current_char().isalpha()):
            return self.alpha()  # method advances sufficiently
        self.error()


def lex(text):
    lexer = Lexer(text)
    tokens = []
    nextToken = lexer.get_next_token()
    while nextToken.type is not EOF:
        tokens.append(nextToken)
        nextToken = lexer.get_next_token()
    return tokens
