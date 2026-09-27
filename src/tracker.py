import os
import urllib.parse
import urllib.request
from typing import List, Tuple
from .bencode import bdecode

def generate_peer_id() -> bytes:
    prefix = b"-PY0001-"
    random_bytes = os.urandom(12)
    return prefix + random_bytes


def build_tracker_url(announce_url: str, info_hash: bytes, peer_id: bytes, port: int = 6881, total_length: int = 0) -> str:
    params = {
        "info_hash": info_hash,
        "peer_id": peer_id,
        "port": port,
        "uploaded": 0,
        "downloaded": 0,
        "left": total_length,
        "compact": 1,
        "event": "started",
    }
    encoded_params = urllib.parse.urlencode(params)
    delimiter = "&" if "?" in announce_url else "?"
    return f"{announce_url}{delimiter}{encoded_params}"

def parse_peers_compact(peers_binary: bytes) -> List[Tuple[str, int]]:
    peers = []
    for i in range(0, len(peers_binary), 6):
        chunk = peers_binary[i : i + 6]
        if len(chunk) < 6:
            break
        ip = ".".join(str(b) for b in chunk[:4])
        port = int.from_bytes(chunk[4:], byteorder="big")
        peers.append((ip, port))
    return peers

def request_peers_http(announce_url: str, info_hash: bytes, peer_id: bytes, total_length: int = 0) -> List[Tuple[str, int]]:
    if not announce_url.startswith("http://") and not announce_url.startswith("https://"):
        raise ValueError(f"Protocolo de tracker não suportado: {announce_url}")

    url = build_tracker_url(announce_url, info_hash, peer_id, total_length=total_length)
    req = urllib.request.Request(url, headers={"User-Agent": "PyTorrent/1.0"})
    
    with urllib.request.urlopen(req, timeout=10) as response:
        response_bytes = response.read()

    decoded = bdecode(response_bytes)
    if b"failure reason" in decoded:
        reason = decoded[b"failure reason"].decode("utf-8")
        raise RuntimeError(f"Erro no Tracker: {reason}")

    peers_data = decoded.get(b"peers", b"")
    if isinstance(peers_data, bytes):
        return parse_peers_compact(peers_data)
    elif isinstance(peers_data, list):
        return [(p[b"ip"].decode("utf-8"), p[b"port"]) for p in peers_data]
    return []
