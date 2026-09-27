import unittest
from src.bencode import bdecode, bencode


class TestBencode(unittest.TestCase):

    def test_bdecode_integer(self):
        self.assertEqual(bdecode(b"i42e"), 42)
        self.assertEqual(bdecode(b"i-7e"), -7)

    def test_bdecode_string(self):
        self.assertEqual(bdecode(b"4:wiki"), b"wiki")
        self.assertEqual(bdecode(b"0:"), b"")

    def test_bdecode_list(self):
        self.assertEqual(bdecode(b"l4:wikii42ee"), [b"wiki", 42])

    def test_bdecode_dict(self):
        expected = {b"bar": b"spam", b"foo": 42}
        self.assertEqual(bdecode(b"d3:bar4:spam3:fooi42ee"), expected)

    def test_bencode_encode(self):
        self.assertEqual(bencode(42), b"i42e")
        self.assertEqual(bencode("wiki"), b"4:wiki")
        self.assertEqual(bencode([b"wiki", 42]), b"l4:wikii42ee")


if __name__ == "__main__":
    unittest.main()
