import unittest

from lisptranslator import translate

class TestTranslator(unittest.TestCase):
  def test_1(self):
    self.assertEqual(translate('2 + 3'), '(+ 2 3)')
  def test_2(self):
    self.assertEqual(translate('(2 + 3 * 5)'), '(+ 2 (* 3 5))')

if __name__ == '__main__':
  unittest.main()
