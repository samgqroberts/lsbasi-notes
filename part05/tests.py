import unittest

target = __import__("interpreter")
Interpreter = target.Interpreter

class TestInterpreter(unittest.TestCase):
  def test_interpreter_1(self):
    self.assertEqual(Interpreter('12 + 3 * 3 - 10 / 2').expr(), 12 + 3 * 3 - 10 / 2)
  def test_interpreter_2(self):
    self.assertEqual(Interpreter('   12  ').expr(), 12)
  def test_interpreter_3(self):
    self.assertEqual(Interpreter('4*12+2').expr(), 50)

if __name__ == '__main__':
  unittest.main()
