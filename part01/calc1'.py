# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, MINUS, EOF = 'INTEGER', 'MINUS', 'EOF'


class Token(object):
  def __init__(self, type, value):
    # token type: INTEGER, MINUS or EOF
    self.type = type
    # token value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', or None
    self.value = value
  
  def __str__(self):
    """String representation of the class instance.

    Examples:
      Token(INTEGER, 3)
      Token(MINUS, '-')
    """
    return 'Token({type}, {value})'.format(
      type=self.type,
      value=repr(self.value)
    )
  
  def __repr__(self):
    return self.__str__()


class Interpreter(object):
  def __init__(self, text):
    # client string input, e.g. "3+5"
    self.text = text
    # self.pos is an index into self.text
    self.pos = 0
    # current token instance
    self.current_token = None
  
  def error(self):
    raise Exception('Error parsing input')

  def skip_whitespace(self):
    while (self.pos < len(self.text)):
      if self.text[self.pos].isspace():
        self.pos += 1
      else:
        break

  def get_next_token(self):
    """Lexical analyzer (also known as scanner or tokenizer)

    This method is responsible for breaking a sentence
    apart into tokens. One token at a time.
    """
    text = self.text

    # move ahead to the next non-whitespace character
    self.skip_whitespace()

    # is self.pos index past the end of self.text ?
    # if so, then return  EOF token because there is no more
    # input left to convert into tokens
    if self.pos > len(text) - 1:
      return Token(EOF, None)
    
    # get a character at the position self.pos and decide
    # what token to create based on the single character
    current_char = text[self.pos]

    # if the character is a digit then convert it to
    # integer, create an INTEGER token, increment self.pos
    # index to point to the next character after the digit,
    # and return the INTEGER token
    if current_char.isdigit():
      num = ''
      while (self.pos < len(text)):
        current_char = text[self.pos]
        if current_char.isdigit():
          num += current_char
          self.pos += 1
        else:
          break
      token = Token(INTEGER, int(num))
      return token
    
    if current_char == '-':
      token = Token(MINUS, current_char)
      self.pos += 1
      return token

    
    self.error()

  def eat(self, token_type):
    # compare the current token type with the passed token
    # type and if they match then "eat" the current token
    # and assign the next token to the self.current_token,
    # otherwise raise an exception.
    if self.current_token.type == token_type:
      self.current_token = self.get_next_token()
    else:
      self.error()
  
  def expr(self):
    """expr -> INTEGER MINUS INTEGER"""
    # set current token to the first token taken from the input
    self.current_token = self.get_next_token()

    # we expect the current token to be a single-digit integer
    left = self.current_token
    self.eat(INTEGER)

    # we expect the current token to be a '-' token
    op = self.current_token
    self.eat(MINUS)

    # we expect the current token to be a single-digit integer
    right = self.current_token
    self.eat(INTEGER)
    # after the above call the self.current_token is set to
    # EOF token

    # at this point INTEGER MINUS INTEGER sequence of tokens
    # has been successfully found and the method can just
    # return the result of adding two integers, thus
    # effectively interpreting client input
    result = left.value - right.value
    return result


def main():
  while True:
    try:
      # To run under Python3 replace 'raw_input' call
      # with 'input'
      text = input('calc> ')
    except EOFError:
      break
    if not text:
      continue
    interpreter = Interpreter(text)
    result = interpreter.expr()
    print(result)

if __name__ == '__main__':
  main()

""" Check your understanding
1. What is an interpreter? A program that takes a representation of code
   and evaluates it.
2. What is a compiler? A program that takes a representation of code and
   produces machine code.
3. What’s the difference between an interpreter and a compiler?
   An interpreter will evaluate code directly, a compiler produces another
   representation of the code (to be evaluated later)
4. What is a token?
   A unit of semantic meaning in written code. Could be represented by
   one or more text characters.
5. What is the name of the process that breaks input apart into tokens?
   Lexical analysis, or lexing.
6. What is the part of the interpreter that does lexical analysis called?
   Lexical analyzer, or lexer.
7. What are the other common names for that part of an interpreter or a compiler?
   scanner, tokenizer