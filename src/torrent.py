import hashlib
from typing import Dict, List, Any
from .bencode import bdecode


def extract_info_hash_raw(raw_data: bytes) -> bytes:
    key = b"4:info"
    key_pos = raw_data.find(key)
    if key_pos == -1:
        raise ValueError("Chave 'info' não encontrada no arquivo .torrent.")

    start_pos = key_pos + len(key)

    def get_end_index(data: bytes, index: int) -> int:
        char = data[index : index + 1]
        if char == b"i":
            return data.find(b"e", index) + 1
        elif char.isdigit():
            colon = data.find(b":", index)
            length = int(data[index:colon])
            return colon + 1 + length
        elif char in (b"l", b"d"):
            curr = index + 1
            while data[curr : curr + 1] != b"e":
                curr = get_end_index(data, curr)
                if char == b"d":
                    curr = get_end_index(data, curr)
            return curr + 1
        raise ValueError("Estrutura bencode malformada ao analisar limite de 'info'.")

    end_pos = get_end_index(raw_data, start_pos)
    raw_info_bytes = raw_data[start_pos:end_pos]
    return hashlib.sha1(raw_info_bytes).digest()

class Torrent:

    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, "rb") as f:
            self.raw_data = f.read()

        self.decoded_data: Dict[bytes, Any] = bdecode(self.raw_data)
        self.info_hash: bytes = extract_info_hash_raw(self.raw_data)

    @property
    def announce(self) -> str:
        return self.decoded_data.get(b"announce", b"").decode("utf-8")

    @property
    def announce_list(self) -> List[str]:
        trackers = []
        if b"announce" in self.decoded_data:
            trackers.append(self.announce)

        if b"announce-list" in self.decoded_data:
            for tier in self.decoded_data[b"announce-list"]:
                for tracker_bytes in tier:
                    url = tracker_bytes.decode("utf-8")
                    if url not in trackers:
                        trackers.append(url)
        return trackers

    @property
    def name(self) -> str:
        info = self.decoded_data[b"info"]
        return info[b"name"].decode("utf-8")

    @property
    def piece_length(self) -> int:
        return self.decoded_data[b"info"][b"piece length"]

    @property
    def total_length(self) -> int:
        info = self.decoded_data[b"info"]
        if b"length" in info:
            return info[b"length"]
        return sum(f[b"length"] for f in info[b"files"])
