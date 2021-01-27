""" Grammar

expr : term ((PLUS | MIN) term)*
term : factor ((MULT | DIV) factor)*
factor : INTEGER
"""

INTEGER, PLUS, MIN, MULT, DIV, EOF = 'INTEGER', 'PLUS', 'MIN', 'MULT', 'DIV', 'EOF'

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
  
  def log(self, additional):
    print(additional, "|| pos: %s, cur: '%s', rem: '%s'" % (self.pos, self.current_char(), self.text[self.pos:]))
  
  def current_char(self):
    if self.pos >= len(self.text):
      return None
    return self.text[self.pos]
  
  def advance(self):
    self.pos += 1

  def integer(self):
    result = ''
    while self.current_char() is not None and self.current_char().isdigit():
      result += self.current_char()
      self.advance()
    return int(result)

  def skip_whitespace(self):
    while self.current_char() is not None and self.current_char().isspace():
      self.advance()

  def get_next_token(self):
    self.log("get_next_token")
    
    self.skip_whitespace()

    token = None
    current_char = self.current_char()
    if current_char is None:
      token = Token(EOF, '')
    elif current_char.isdigit():
      token = Token(INTEGER, self.integer())
    elif current_char == '+':
      self.advance()
      token = Token(PLUS, '+')
    elif current_char == '-':
      self.advance()
      token = Token(MIN, '-')
    elif current_char == '*':
      self.advance()
      token = Token(MULT, '*')
    elif current_char == '/':
      self.advance()
      token = Token(DIV, '/')

    if token is None:
      self.error('Could not match next token with any known lexeme')
    
    return token
  
  def error(self, cause):
    raise Exception(cause)


class Interpreter():
  def __init__(self, text):
    self.lexer = Lexer(text)
    self.current_token = self.lexer.get_next_token()
  
  def error(self, cause):
    raise Exception(cause)
  
  def eat(self, type):
    self.log("eat")
    if self.current_token.type == type:
      self.current_token = self.lexer.get_next_token()
      self.log("eat returning")
    else:
      self.error("Expected current token to be type %s, found %s" % (type, self.current_token.type))
  
  def plus(self):
    self.log("plus")
    self.eat(PLUS)
    self.log("plus after")
  
  def min(self):
    self.eat(MIN)
  
  def mult(self):
    self.eat(MULT)
  
  def div(self):
    self.eat(DIV)
  
  def factor(self):
    self.log("factor")
    value = self.current_token.value
    self.eat(INTEGER)
    return value
  
  def log(self, addition):
    print(addition, "|| Current token: %s" % self.current_token)
  
  def term(self):
    self.log("term")
    result = self.factor()

    while self.current_token.type in (MULT, DIV):
      if self.current_token.type == MULT:
        self.mult()
        result *= self.factor()
      if self.current_token.type == DIV:
        self.div()
        result /= self.factor()
    
    self.log("term returning %s" % result)
    return result
  
  def expr(self):
    self.log("expr")
    result = self.term()

    while self.current_token.type in (PLUS, MIN):
      if self.current_token.type == PLUS:
        self.plus()
        result += self.term()
      if self.current_token.type == MIN:
        self.min()
        result -= self.term()
    
    return result

