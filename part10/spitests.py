import unittest

from spi import lex, Token, INTEGER, PLUS, MINUS, LPAREN, REAL, RPAREN  # , parse, evaluate

sample_program = open("part10.pas", "r").read()


class TestSuite(unittest.TestCase):
    def test_lexer_simple(self):
        text = " 1 + 2 -   (-3.4) "
        tokens = lex(text)
        expected = [
            Token(INTEGER, 1),
            Token(PLUS, '+'),
            Token(INTEGER, 2),
            Token(MINUS, '-'),
            Token(LPAREN, '('),
            Token(MINUS, '-'),
            Token(REAL, 3.4),
            Token(RPAREN, ')')
        ]
        self.assertEqual(tokens, expected)


if __name__ == '__main__':
    unittest.main()
