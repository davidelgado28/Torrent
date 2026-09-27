import unittest
import hashlib
from src.bencode import bencode
from src.torrent import extract_info_hash_raw


class TestTorrent(unittest.TestCase):

    def test_extract_info_hash_raw(self):
        info_dict = {
            b"name": b"test.txt",
            b"piece length": 32768,
            b"pieces": b"12345678901234567890",
            b"length": 100,
        }
        encoded_info = bencode(info_dict)
        raw_data = b"d8:announce34:http://tracker.example.com/announce4:info" + encoded_info + b"e"

        expected_hash = hashlib.sha1(encoded_info).digest()
        extracted_hash = extract_info_hash_raw(raw_data)

        self.assertEqual(extracted_hash, expected_hash)


if __name__ == "__main__":
    unittest.main()
