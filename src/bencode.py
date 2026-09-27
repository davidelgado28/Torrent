def bdecode(data: bytes):

    def parse(index: int):
        if index >= len(data):
            raise ValueError("Fim inesperado dos dados durante o parsing.")

        char = data[index : index + 1]

        if char == b"i":
            end = data.find(b"e", index)
            if end == -1:
                raise ValueError("Inteiro Bencode malformado: 'e' ausente.")
            val = int(data[index + 1 : end])
            return val, end + 1

        elif char.isdigit():
            colon = data.find(b":", index)
            if colon == -1:
                raise ValueError("String Bencode malformada: ':' ausente.")
            length = int(data[index:colon])
            start = colon + 1
            end = start + length
            if end > len(data):
                raise ValueError("Comprimento da string excede os dados disponíveis.")
            return data[start:end], end

        elif char == b"l":
            curr = index + 1
            elements = []
            while data[curr : curr + 1] != b"e":
                element, curr = parse(curr)
                elements.append(element)
            return elements, curr + 1

        elif char == b"d":
            curr = index + 1
            dictionary = {}
            while data[curr : curr + 1] != b"e":
                key, curr = parse(curr)
                value, curr = parse(curr)
                dictionary[key] = value
            return dictionary, curr + 1

        else:
            raise ValueError(f"Símbolo Bencode inválido no índice {index}: {char}")

    result, _ = parse(0)
    return result


def bencode(val) -> bytes:
    if isinstance(val, int):
        return f"i{val}e".encode("utf-8")
    elif isinstance(val, str):
        val_bytes = val.encode("utf-8")
        return f"{len(val_bytes)}:".encode("utf-8") + val_bytes
    elif isinstance(val, bytes):
        return f"{len(val)}:".encode("utf-8") + val
    elif isinstance(val, list):
        return b"l" + b"".join(bencode(item) for item in val) + b"e"
    elif isinstance(val, dict):
        encoded_dict = b"d"
        sorted_keys = sorted(
            val.keys(),
            key=lambda k: k if isinstance(k, bytes) else str(k).encode("utf-8")
        )
        for k in sorted_keys:
            key_bytes = k if isinstance(k, bytes) else str(k).encode("utf-8")
            encoded_dict += bencode(key_bytes) + bencode(val[k])
        return encoded_dict + b"e"
    else:
        raise TypeError(f"Tipo não suportado para Bencode: {type(val)}")
