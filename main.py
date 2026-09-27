import sys
import os
from src.torrent import Torrent

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_do_arquivo.torrent>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        sys.exit(1)

    try:
        torrent = Torrent(file_path)

        print("=" * 50)
        print(" METADADOS DO ARQUIVO .TORRENT")
        print("=" * 50)
        print(f"Nome do Conteúdo : {torrent.name}")
        print(f"Tamanho Total    : {torrent.total_length:,} bytes")
        print(f"Tamanho de Peça  : {torrent.piece_length:,} bytes")
        print(f"Info Hash (Hex)  : {torrent.info_hash.hex()}")
        print("-" * 50)
        print("Trackers Encontrados:")
        for idx, tracker in enumerate(torrent.announce_list, 1):
            print(f"  {idx}. {tracker}")
        print("=" * 50)

    except Exception as e:
        print(f"Erro ao processar o arquivo .torrent: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
