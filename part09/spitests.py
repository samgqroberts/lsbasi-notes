import unittest
from unittest.case import expectedFailure

from spi import evaluate

TEST_PROGRAM = """
BEGIN
    BEGIN
        number := 2;
        a := number;
        b := 10 * a + 10 * number div 4;
        c := a - - b
    END;
    x := 11;
END.
"""

EXPECTED_GLOBAL_SCOPE = {'NUMBER': 2, 'A': 2, 'B': 25, 'C': 27, 'X': 11}

class TestTranslator(unittest.TestCase):
  def test_basic(self):
    eval_testprogram = evaluate(TEST_PROGRAM)
    self.assertEqual(eval_testprogram, EXPECTED_GLOBAL_SCOPE)
  def test_case_insensitivity(self):
    insensitive = """
BEGIN

    BEGIN
        number := 2;
        a := NumBer;
        B := 10 * a + 10 * NUMBER div 4;
        c := a - - b
    end;

    x := 11;
END.
    """
    eval_insensitive = evaluate(insensitive)
    self.assertEqual(eval_insensitive, EXPECTED_GLOBAL_SCOPE)

if __name__ == '__main__':
  unittest.main()

