from multiformats import multihash


class Multihashing:
    def __init__(self, hash_function: str):
        self.hash_function = multihash.Multihash(hash_function)

    def __call__(self, data: bytes) -> bytes:
        return multihash.digest(data, self.hash_function)
