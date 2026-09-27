def create_handshake(info_hash: bytes, peer_id: bytes) -> bytes:
    pstr = b"BitTorrent protocol"
    pstrlen = bytes([len(pstr)])
    reserved = b"\x00" * 8

    if len(info_hash) != 20 or len(peer_id) != 20:
        raise ValueError("Info Hash e Peer ID devem ter exatamente 20 bytes.")

    return pstrlen + pstr + reserved + info_hash + peer_id

def parse_handshake(data: bytes) -> dict:
    if len(data) < 68:
        raise ValueError("Handshake incompleto (mínimo 68 bytes).")

    pstrlen = data[0]
    pstr = data[1 : 1 + pstrlen]
    if pstr != b"BitTorrent protocol":
        raise ValueError(f"Protocolo inválido: {pstr}")

    reserved = data[1 + pstrlen : 1 + pstrlen + 8]
    info_hash = data[1 + pstrlen + 8 : 1 + pstrlen + 8 + 20]
    peer_id = data[1 + pstrlen + 8 + 20 : 1 + pstrlen + 8 + 20 + 20]

    return {
        "pstr": pstr,
        "reserved": reserved,
        "info_hash": info_hash,
        "peer_id": peer_id,
    }
