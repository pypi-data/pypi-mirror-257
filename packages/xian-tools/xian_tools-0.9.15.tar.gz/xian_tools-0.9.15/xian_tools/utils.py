import base64
import struct
import json

from typing import Dict, Any


def decode_dict(encoded_dict: str) -> Dict[str, Any]:
    decoded_data = decode_str(encoded_dict)
    decoded_tx = bytes.fromhex(decoded_data).decode('utf-8')
    return json.loads(decoded_tx)


def decode_str(encoded_data: str) -> str:
    decoded_bytes = base64.b64decode(encoded_data)
    return decoded_bytes.decode('utf-8')


def decode_int(encoded_int: str) -> int:
    decoded_bytes = base64.b64decode(encoded_int)
    value = struct.unpack('>i', decoded_bytes)[0]
    return int(value)


def decode_float(encoded_int: str) -> float:
    decoded_bytes = base64.b64decode(encoded_int)
    value = struct.unpack('>d', decoded_bytes)[0]
    return float(value)


def cid():
    return 'xian-testnet-1'
