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


class AST(object):
    pass


class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block

    def __repr__(self):
        return 'Program(' + str(self.name) + ', ' + str(self.block) + ')'

    def __eq__(self, obj):
        return isinstance(obj, Program) and obj.name == self.name and obj.block == self.block


class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

    def __repr__(self):
        return 'Block(' + str(self.declarations) + ', ' + str(self.compound_statement) + ')'

    def __eq__(self, obj):
        return isinstance(obj, Block) and obj.declarations == self.declarations and obj.compound_statement == self.compound_statement


class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Compound(AST):
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return 'Compound(' + str(self.children) + ')'

    def __eq__(self, obj):
        return isinstance(obj, Compound) and obj.children == self.children


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg):
        raise Exception('Error parsing: ' + msg)

    def eat(self, type):
        if self.current_token.type != type:
            self.error('Expected current token to be ' + type +
                       '. Found: ' + self.current_token.type)
        node = self.current_token
        self.current_token = self.lexer.get_next_token()
        return node

    def program(self):
        self.eat(PROGRAM)
        var = self.variable()
        self.eat(SEMI)
        block = self.block()
        self.eat(DOT)
        return Program(var.value, block)

    def block(self):
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        return Block(declarations, compound_statement)

    def declarations(self):
        decls = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            while (self.current_token.type == ID):
                decls.append(self.variable_declaration())
                self.eat(SEMI)
        return decls

    def variable_declaration(self):
        pass

    def type_spec(self):
        pass

    def compound_statement(self):
        self.eat(BEGIN)
        stmt_list = self.statement_list()
        self.eat(END)
        return Compound(stmt_list)

    def statement_list(self):
        return []

    def statement(self):
        pass

    def assignment_statement(self):
        pass

    def empty(self):
        pass

    def expr(self):
        pass

    def term(self):
        pass

    def factor(self):
        pass

    def variable(self):
        node = self.eat(ID)
        return Var(node)

    def parse(self):
        node = self.program()
        if (self.current_token.type is not EOF):
            self.error(
                'Parsed program, but next token is not EOF. Found: ' + str(self.current_token))
        return node


def parse(text):
    lexer = Lexer(text)
    return Parser(lexer).parse()
