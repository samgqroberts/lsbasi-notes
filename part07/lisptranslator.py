"""
Write a translator (hint: node visitor) that takes as input an arithmetic expression
and prints it out in postfix notation, also known as Reverse Polish Notation (RPN).
For example, if the input to the translator is the expression (5 + 3) * 12 / 3
than the output should be 5 3 + 12 * 3 /. See the answer here but try to solve it
first on your own.
"""

"""
"" LEXER
"""

INT, ADD, SUBT, MULT, DIV, LPAR, RPAR, EOF = 'INT', 'ADD', 'SUBT', 'MULT', 'DIV', 'LPAR', 'RPAR', 'EOF'

class Token():
  def __init__(self, type, value):
    self.type = type
    self.value = value

  def __repr__(self):
    return '%s(%s)' % (self.type, self.value)

class Lexer():
  def __init__(self, text):
    self.text = text
    self.pos = 0
    self.current_char = self.get_cur_char()
  
  def get_cur_char(self):
    if (len(self.text) > self.pos):
      return self.text[self.pos]
    return None
  
  def advance(self):
    self.pos += 1
    self.current_char = self.get_cur_char()
  
  def cur_char_is_whitespace(self):
    return self.current_char is not None and self.current_char.isspace()
  
  def skip_whitespace(self):
    while (self.cur_char_is_whitespace()):
      self.advance()
  
  def cur_char_is_digit(self):
    return self.current_char is not None and self.current_char.isdigit()
  
  def integer(self):
    value = ''
    while (self.cur_char_is_digit()):
      value += self.current_char
      self.advance()
    return int(value)
  
  # returns a Token
  def get_next_token(self):
    if (self.cur_char_is_whitespace):
      self.skip_whitespace()

    if (self.current_char == None):
      return Token(EOF, '')
    
    if (self.current_char.isdigit()):
      return Token(INT, self.integer())
    
    if (self.current_char == '+'):
      self.advance()
      return Token(ADD, '+')
    if (self.current_char == '-'):
      self.advance()
      return Token(SUBT, '-')
    if (self.current_char == '*'):
      self.advance()
      return Token(MULT, '*')
    if (self.current_char == '/'):
      self.advance()
      return Token(DIV, '/')
    if (self.current_char == '('):
      self.advance()
      return Token(LPAR, '(')
    if (self.current_char == ')'):
      self.advance()
      return Token(RPAR, ')')
    
    raise Exception('Cannot recognize charactor {}'.format(self.current_char))

"""
"" Parser
"""

class AST():
  pass

class BinOp(AST):
  def __init__(self, left, op, right):
    self.left = left
    self.op = op
    self.right = right
  def __repr__(self):
    return 'BinOp(%s,%s,%s)' % (self.left, self.op, self.right)

class Num(AST):
  def __init__(self, value):
    self.value = value
  def __repr__(self):
    return 'Num(%s)' % (self.value)

class Parser():
  def __init__(self, lexer):
    self.lexer = lexer
    self.current_token = self.lexer.get_next_token()
  
  def eat(self, type):
    if (self.current_token.type != type):
      raise Exception('Expected token of type {}, got {}'.format(type, self.current_token.type))
    self.current_token = self.lexer.get_next_token()
  
  def factor(self):
    if (self.current_token.type == LPAR):
      self.eat(LPAR)
      node = self.expr()
      self.eat(RPAR)
      return node
    else:
      value = self.current_token
      self.eat(INT)
      return Num(value)

  def term(self):
    node = self.factor()

    while (self.current_token.type in (MULT, DIV)):
      token = self.current_token
      if (self.current_token.type == MULT):
        self.eat(MULT)
      if (self.current_token.type == DIV):
        self.eat(DIV)
      node = BinOp(left=node, op=token, right=self.factor())
    
    return node

  def expr(self):
    node = self.term()

    while (self.current_token.type in (ADD, SUBT)):
      token = self.current_token
      if (self.current_token.type == ADD):
        self.eat(ADD)
      if (self.current_token.type == SUBT):
        self.eat(SUBT)
      node = BinOp(left=node, op=token, right=self.term())
    
    return node

  
  # returns an AST
  def parse(self):
    return self.expr()


class NodeVisitor():
  def visit(self, node):
    method_name = 'visit_' + type(node).__name__
    visitor = getattr(self, method_name, self.generic_visit)
    return visitor(node)
  
  def generic_visit(self, node):
    raise Exception('No visit_{} method'.format(type(node).__name__))

class Translator(NodeVisitor):
  def __init__(self, parser):
    self.parser = parser
  
  def visit_BinOp(self, node):
    print('visiting binop {}'.format(node))
    left = self.visit(node.left)
    right = self.visit(node.right)
    op = node.op.value
    value = '(' + op + ' ' + left + ' ' + right + ')'
    print('binop value "{}"'.format(value))
    return value
  
  def visit_Num(self, node):
    value = str(node.value.value)
    print('visiting num {}'.format(node))
    return value
  
  def translate(self):
    ast = self.parser.parse()
    value = self.visit(ast)
    print('overall value "{}"'.format(value))
    return value

def translate(input):
  lexer = Lexer(input)
  parser = Parser(lexer)
  translator = Translator(parser)
  return translator.translate()