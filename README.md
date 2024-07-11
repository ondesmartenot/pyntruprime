# pyntruprime
A Python wrapper for the libntruprime microlibrary

# Installation
## Dependencies
pyntruprime depends only on libntruprime (which also depends on libcpucycles and
librandombytes), available [here](https://lib.ntruprime.org)

# API
## Instantiated parameters
The API follows the libntruprime API. It implements the following parameter sets:

- sntrup761

More parameter sets may be added later

Each has the following constants defined:
- sntrup761.PUBLICKEYBYTES
Length of the public key
- sntrup761.SECRETKEYBYTES
Length of the private key
- sntrup761.CIPHERTEXTBYTES
Length of the ciphertext
- sntrup761.BYTES
Length of the session key

## Usage
For each instantiation the following functions are available:
### sntrup761.keypair() -> Tuple[bytes, bytes]

Randomly generates a NTRUprime secret key and its corresponding public key.

Example:
```python
>>> from pyntruprime import sntrup761
>>> pk, sk = sntrup761.keypair()
```

### sntrup761.enc(pk: bytes) -> Tuple[bytes, bytes]
Randomly generates a ciphertext and the corresponding session key given a
public key pk.

Example:
```python
>>> from pyntruprime import sntrup761
>>> pk, _ = sntrup761.keypair()
>>> c, k = sntrup761.enc(pk)
```

### sntrup761.dec(c: bytes, pk: bytes) -> bytes
Given a NTRUprime secret key sk and a ciphertext c encapsulated to sk's
corresponding public key pk, computes the session key k.

Example:
```python
>>> from pyntruprime import sntrup761
>>> pk, sk = sntrup761.keypair()
>>> c, k = sntrup761.enc(pk)
>>> sntrup761.dec(c, sk) == k
True
```
