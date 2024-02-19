import unittest


class TestGetMethod(unittest.TestCase):
    def setUp(self) -> None:
        import pathlib
        import sys
        sys.path[0] = (pathlib.Path(__file__).parent.parent / 'src').__str__()

    def test_get_existing_tag(self):
        import boj.tags
        x = boj.tags.get(1)
        self.assertIsInstance(x, boj.tags.Tag)

    def test_get_non_existing_tag(self):
        import boj.tags
        with self.assertRaises(Exception):
            boj.tags.get(99999)


if __name__ == '__main__':
    unittest.main()
