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

    def __repr__(self):
        return 'VarDecl(' + str(self.var_node) + ', ' + str(self.type_node) + ')'

    def __eq__(self, obj):
        return isinstance(obj, VarDecl) and obj.var_node == self.var_node and obj.type_node == self.type_node


class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return 'Type(' + str(self.token) + ', ' + str(self.token) + ')'

    def __eq__(self, obj):
        return isinstance(obj, Type) and obj.token == self.token and obj.value == self.value


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

    def __repr__(self):
        return 'Assign(' + str(self.left) + ', ' + str(self.token) + ', ' + str(self.right) + ')'

    def __eq__(self, obj):
        return isinstance(obj, Assign) and obj.left == self.left and obj.token == self.token and obj.right == self.right


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self):
        return 'BinOp(' + str(self.left) + ', ' + str(self.token) + ', ' + str(self.right) + ')'

    def __eq__(self, obj):
        return isinstance(obj, BinOp) and obj.left == self.left and obj.token == self.token and obj.right == self.right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return 'Num(' + str(self.token) + ', ' + str(self.value) + ')'

    def __eq__(self, obj):
        return isinstance(obj, Num) and obj.token == self.token and obj.value == self.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __repr__(self):
        return 'UnaryOp(' + str(self.token) + ', ' + str(self.expr) + ')'

    def __eq__(self, obj):
        return isinstance(obj, UnaryOp) and obj.token == self.token and obj.expr == self.expr


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return 'Var(' + str(self.token) + ', ' + str(self.value) + ')'

    def __eq__(self, obj):
        return isinstance(obj, Var) and obj.token == self.token and obj.value == self.value


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
                decls += self.variable_declaration()
                self.eat(SEMI)
        return decls

    def variable_declaration(self):
        vars = [self.variable()]
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            vars.append(self.variable())
        self.eat(COLON)
        type = self.type_spec()
        return [VarDecl(var, type) for var in vars]

    def type_spec(self):
        if self.current_token.type == INTEGER:
            return Type(self.eat(INTEGER))
        if self.current_token.type == REAL:
            return Type(self.eat(REAL))
        self.error()

    def compound_statement(self):
        self.eat(BEGIN)
        stmt_list = self.statement_list()
        if self.current_token.type == SEMI:
            self.eat(SEMI)
        self.eat(END)
        return Compound(stmt_list)

    def statement_list(self):
        stmts = [self.statement()]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            stmts.append(self.statement())
        return stmts

    def statement(self):
        if (self.current_token.type == BEGIN):
            return self.compound_statement()
        if (self.current_token.type == ID):
            return self.assignment_statement()
        return self.empty()

    def assignment_statement(self):
        left = self.variable()
        token = self.eat(ASSIGN)
        right = self.expr()
        return Assign(left, token, right)

    def empty(self):
        pass

    def expr(self):
        node = self.term()
        while self.current_token.type in [PLUS, MINUS]:
            if self.current_token.type == PLUS:
                token = self.eat(PLUS)
            if self.current_token.type == MINUS:
                token = self.eat(MINUS)
            node = BinOp(node, token, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in [MUL, INTEGER_DIV, FLOAT_DIV]:
            if self.current_token.type == MUL:
                token = self.eat(MUL)
            if self.current_token.type == INTEGER_DIV:
                token = self.eat(INTEGER_DIV)
            if self.current_token.type == FLOAT_DIV:
                token = self.eat(FLOAT_DIV)
            node = BinOp(node, token, self.factor())
        return node

    def factor(self):
        if self.current_token.type == PLUS:
            return UnaryOp(self.eat(PLUS), self.factor())
        if self.current_token.type == MINUS:
            return UnaryOp(self.eat(MINUS), self.factor())
        if self.current_token.type == INTEGER_CONST:
            return Num(self.eat(INTEGER_CONST))
        if self.current_token.type == REAL_CONST:
            return Num(self.eat(REAL_CONST))
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        if self.current_token.type == ID:
            return Var(self.eat(ID))
        self.error('unexpected factor. current token: ' +
                   str(self.current_token))

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
