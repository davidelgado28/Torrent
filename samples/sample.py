import os
from src.bencode import bencode

def create_dummy_torrent():
    os.makedirs("samples", exist_ok=True)

    torrent_data = {
        b"announce": b"http://tracker.example.com/announce",
        b"info": {
            b"name": b"readme_teste.txt",
            b"piece length": 16384,  
            b"pieces": b"12345678901234567890", 
            b"length": 1024,        
        }
    }
    raw_torrent = bencode(torrent_data)
    file_path = "samples/sample.torrent"
    with open(file_path, "wb") as f:
        f.write(raw_torrent)

    print(f"Arquivo gerado com sucesso em: {file_path}")

if __name__ == "__main__":
    create_dummy_torrent()
