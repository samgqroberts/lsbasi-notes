import unittest

from postfixtranslator import translate

class TestTranslator(unittest.TestCase):
  def test_1(self):
    self.assertEqual(translate('5 + 3'), '5 3 +')
  def test_2(self):
    self.assertEqual(translate('(5 + 3) * 12 / 3'), '5 3 + 12 * 3 /')

if __name__ == '__main__':
  unittest.main()
