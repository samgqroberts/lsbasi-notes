### Testing in Python

Here's a minimal test suite, using the unittest package:

```
import unittest

class TestSuite(unittest.TestCase):
    def test_case(self):
        self.assertEqual(1 + 2, 3)

if __name__ == '__main__':
    unittest.main()
```

To it you just run python on the file:

```
python3 tests.py
```

To run it with a watch cycle you can use `nodemon`:

```
nodemon --exec python3 tests.py
```