"""Unit tests: python -m unittest -v test_quicksort.py"""
import random
import unittest
from quicksort import quicksort, randomized_quicksort

class QuicksortTests(unittest.TestCase):
    def test_cases(self):
        cases = [[], [1], [2, 1], [4, 4, 4], [-3, 2, -1, 0],
                 list(range(250)), list(range(249, -1, -1)),
                 [random.Random(42).randrange(5) for _ in range(300)]]
        for fn in (quicksort, randomized_quicksort):
            for case in cases:
                with self.subTest(algorithm=fn.__name__, case_size=len(case)):
                    values = case.copy()
                    returned = fn(values)
                    self.assertIs(returned, values)
                    self.assertEqual(values, sorted(case))

if __name__ == '__main__':
    unittest.main()
