from multiformats import multibase


class Multibasing:
    def __init__(self, encoding: str):
        self.encoding = encoding

    def encode(self, data: bytes) -> str:
        return multibase.encode(data, self.encoding)

    def decode(self, data: str) -> bytes:
        return multibase.decode(data)

