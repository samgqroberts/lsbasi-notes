import unittest

from interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
  def test_interpreter_1(self):
    self.assertEqual(Interpreter('12 + 3 * 3 - 10 / 2').expr(), 12 + 3 * 3 - 10 / 2)
  def test_interpreter_2(self):
    self.assertEqual(Interpreter('   12  ').expr(), 12)
  def test_interpreter_3(self):
    self.assertEqual(Interpreter('4*12+2').expr(), 50)
  def test_interpreter_4(self):
    self.assertEqual(Interpreter('3 + (4)').expr(), 7)
  def test_interpreter_4(self):
    self.assertEqual(Interpreter('(4)').expr(), 4)
  def test_interpreter_4(self):
    self.assertEqual(Interpreter('3 * (4 + 2)').expr(), 18)
  def test_interpreter_4(self):
    self.assertEqual(Interpreter('7 + 3 * (10 / (12 / (3 + 1) - 1))').expr(), 7 + 3 * (10 / (12 / (3 + 1) - 1)))

if __name__ == '__main__':
  unittest.main()
