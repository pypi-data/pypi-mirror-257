import unittest


class TestProblems(unittest.TestCase):
    def setUp(self) -> None:
        import pathlib
        import sys
        sys.path[0] = (pathlib.Path(__file__).parent.parent / 'src').__str__()

    def test_get_existing_problem(self):
        import boj.problems
        x = boj.problems.get(1000)
        self.assertIsInstance(x, boj.problems.Problem)

    def test_get_non_existing_problem(self):
        import boj.problems
        with self.assertRaises(Exception):
            boj.problems.get(99999)

    def test_problem_tag(self):
        import boj
        prob = boj.problems.get(1000)
        tag = boj.tags.get(124) # math
        self.assertIn(tag, prob.tags)


if __name__ == '__main__':
    unittest.main()
