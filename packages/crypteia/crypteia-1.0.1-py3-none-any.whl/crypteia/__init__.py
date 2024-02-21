from typing import Callable

from .multibasing import Multibasing
from .multihashing import Multihashing


class ToBytes:
    def __init__(self, encoding: str = 'utf-8'):
        self.encoding = encoding

    def __call__(self, data: str) -> bytes:
        return data.encode(self.encoding)


class ToString:
    def __init__(self, encoding: str = 'utf-8'):
        self.encoding = encoding

    def __call__(self, data: bytes) -> str:
        return data.decode(self.encoding)


def compose(to_bytes, multihasher, multibaser) -> Callable[[str], str]:
    def get_hash(data):
        bin_data = to_bytes(data)
        hashed_data = multihasher(bin_data)
        encoded_data = multibaser.encode(hashed_data)
        return encoded_data
    return get_hash
