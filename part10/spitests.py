import unittest

from spi import lex, evaluate, Lexer, Num, parse, VarDecl, Assign, Var, Type, Token, Program, Compound, Block, INTEGER_CONST, PLUS, MINUS, PROGRAM, LPAREN, REAL_CONST, RPAREN, ID, SEMI, VAR, COLON, INTEGER, COMMA, REAL, BEGIN, ASSIGN, MUL, END, FLOAT_DIV, DOT, INTEGER_DIV

sample_program = open("part10.pas", "r").read()


class TestSuite(unittest.TestCase):
    def test_lexer_simple(self):
        text = " 1 + 2 -   (-3.4) "
        tokens = lex(text)
        expected = [
            Token(INTEGER_CONST, 1),
            Token(PLUS, '+'),
            Token(INTEGER_CONST, 2),
            Token(MINUS, '-'),
            Token(LPAREN, '('),
            Token(MINUS, '-'),
            Token(REAL_CONST, 3.4),
            Token(RPAREN, ')')
        ]
        self.assertEqual(tokens, expected)

    def test_lexer_program(self):
        tokens = lex(sample_program)
        expected = [
            Token(PROGRAM, 'PROGRAM'),
            Token(ID, 'Part10'),
            Token(SEMI, ';'),
            Token(VAR, 'VAR'),
            Token(ID, 'number'),
            Token(COLON, ':'),
            Token(INTEGER, 'INTEGER'),
            Token(SEMI, ';'),
            Token(ID, 'a'),
            Token(COMMA, ','),
            Token(ID, 'b'),
            Token(COMMA, ','),
            Token(ID, 'c'),
            Token(COMMA, ','),
            Token(ID, 'x'),
            Token(COLON, ':'),
            Token(INTEGER, 'INTEGER'),
            Token(SEMI, ';'),
            Token(ID, 'y'),
            Token(COLON, ':'),
            Token(REAL, 'REAL'),
            Token(SEMI, ';'),
            Token(BEGIN, 'BEGIN'),
            Token(BEGIN, 'BEGIN'),
            Token(ID, 'number'),
            Token(ASSIGN, ':='),
            Token(INTEGER_CONST, 2),
            Token(SEMI, ';'),
            Token(ID, 'a'),
            Token(ASSIGN, ':='),
            Token(ID, 'number'),
            Token(SEMI, ';'),
            Token(ID, 'b'),
            Token(ASSIGN, ':='),
            Token(INTEGER_CONST, 10),
            Token(MUL, '*'),
            Token(ID, 'a'),
            Token(PLUS, '+'),
            Token(INTEGER_CONST, 10),
            Token(MUL, '*'),
            Token(ID, 'number'),
            Token(INTEGER_DIV, 'DIV'),
            Token(INTEGER_CONST, 4),
            Token(SEMI, ';'),
            Token(ID, 'c'),
            Token(ASSIGN, ':='),
            Token(ID, 'a'),
            Token(MINUS, '-'),
            Token(MINUS, '-'),
            Token(ID, 'b'),
            Token(END, 'END'),
            Token(SEMI, ';'),
            Token(ID, 'x'),
            Token(ASSIGN, ':='),
            Token(INTEGER_CONST, 11),
            Token(SEMI, ';'),
            Token(ID, 'y'),
            Token(ASSIGN, ':='),
            Token(INTEGER_CONST, 20),
            Token(FLOAT_DIV, '/'),
            Token(INTEGER_CONST, 7),
            Token(PLUS, '+'),
            Token(REAL_CONST, 3.14),
            Token(SEMI, ';'),
            Token(END, 'END'),
            Token(DOT, '.')
        ]
        self.assertEqual(tokens, expected)

    def test_parser_simple(self):
        program = """
PROGRAM onevar;

VAR
    x : INTEGER;

BEGIN
    x := 3
END.
    """
        ast = parse(program)
        expected = Program(
            'onevar',
            Block(
                [VarDecl(
                    Var(Token(ID, 'x')),
                    Type(Token(INTEGER, 'INTEGER'))
                )],
                Compound([
                    Assign(Var(Token(ID, 'x')), Token(ASSIGN, ':='),
                           Num(Token(INTEGER_CONST, 3)))
                ])
            )
        )
        self.assertEqual(ast, expected)

    def test_parser_program(self):
        ast = parse(sample_program)
        self.assertNotEqual(ast, None)  # just want to make sure it runs

    def test_interpret_simple(self):
        program = """
PROGRAM onevar;

VAR
    x : INTEGER;

BEGIN
    x := 3
END.
    """
        scope = evaluate(program)
        expected = {'x': 3}
        self.assertEqual(scope, expected)

    def test_interpret_program(self):
        scope = evaluate(sample_program)
        number = 2
        a = number
        b = 10 * a + 10 * number // 4
        c = 2 - - b
        x = 11
        y = 20 / 7 + 3.14
        expected = {
            'number': number,
            'a': a,
            'b': b,
            'c': c,
            'x': x,
            'y': y
        }
        self.assertEqual(scope, expected)


if __name__ == '__main__':
    unittest.main()
