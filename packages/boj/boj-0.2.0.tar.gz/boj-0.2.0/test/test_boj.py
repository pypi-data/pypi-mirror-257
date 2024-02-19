import unittest


class TestImport(unittest.TestCase):
    def setUp(self) -> None:
        import pathlib
        import sys
        sys.path[0] = (pathlib.Path(__file__).parent.parent / 'src').__str__()

    def test_import(self) -> None:
        import boj


if __name__ == '__main__':
    unittest.main()
