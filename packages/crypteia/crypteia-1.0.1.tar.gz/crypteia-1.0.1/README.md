# crypteia

A crafty coder's content-addressing companion for cascading consistency checks with cryptographic cloak and charm in the cosmic chaos of cyberspace.

## usage

```python
from crypteia import Multibasing, Multihashing, ToBytes, compose

get_hash = compose(ToBytes(), Multihash("sha3-224"), Multibase("base58btc"))
data = "Hello, World!"
digest = get_hash(data)
print(digest)
# 'z5dbMfGzi9pjjDf5Uv7bVDqgPPMGAkrRDmEqSoVquB'
```
