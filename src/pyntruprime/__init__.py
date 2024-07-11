from ctypes import (
    CDLL,
    RTLD_GLOBAL,
    byref,
    c_char_p,
    c_int,
    create_string_buffer,
    util,
)
from typing import Tuple

_librb = CDLL(
    "/usr/local/lib/librandombytes.so"
    or util.find_library("randombytes")
    or util.find_library("librandombytes"),
    mode=RTLD_GLOBAL,
)

_lib = CDLL(
    "/usr/local/lib/libntruprime.so"
    or util.find_library("ntruprime")
    or util.find_library("libntruprime")
)

if not _lib._name:
    raise ValueError("Unable to find libntruprime")


class _NTRU:
    def __init__(self) -> None:
        self._PARAMS = "sntrup761"
        self._PUBLICKEYBYTES: int = 1158
        self._SECRETKEYBYTES: int = 1763
        self._CIPHERTEXTBYTES: int = 1039
        self._BYTES: int = 32

        self._c_keypair = getattr(_lib, f"ntruprime_kem_sntrup761_keypair")
        self._c_keypair.argtypes = [c_char_p, c_char_p]
        self._c_keypair.restype = None

        self._c_enc = getattr(_lib, f"ntruprime_kem_sntrup761_enc")
        self._c_enc.argtypes = [c_char_p, c_char_p, c_char_p]
        self._c_enc.restype = None

        self._c_dec = getattr(_lib, f"ntruprime_kem_sntrup761_dec")
        self._c_dec.argtypes = [c_char_p, c_char_p, c_char_p]
        self._c_dec.restype = None

    @property
    def pklen(self) -> int:
        return self._PUBLICKEYBYTES

    @property
    def sklen(self) -> int:
        return self._SECRETKEYBYTES

    def keypair(self) -> Tuple[bytes, bytes]:
        """Randomly generates a Ntruprime secret key and its corresponding
        public key.

        Example:
        >>> from pyntru import sntrup459761
        >>> pk, sk = sntrup459761.keypair()

        """

        sk = create_string_buffer(self._SECRETKEYBYTES)
        pk = create_string_buffer(self._PUBLICKEYBYTES)
        self._c_keypair(pk, sk)
        return pk.raw, sk.raw

    def enc(self, pk: bytes) -> Tuple[bytes, bytes]:
        """Randomly generates a ciphertext and the corresponding session key
        given a public key pk.

        Example:
        >>> from pyntru import sntrup761
        >>> pk, _ = sntrup761.keypair()
        >>> c, k = sntrup761.enc(pk)

        """
        if not isinstance(pk, bytes):
            raise TypeError("public key must be bytes")
        if len(pk) != self._PUBLICKEYBYTES:
            raise ValueError("invalid public key length")

        c = create_string_buffer(self._CIPHERTEXTBYTES)
        k = create_string_buffer(self._BYTES)
        pk_arr = create_string_buffer(pk)
        self._c_enc(c, k, pk_arr)
        return c.raw, k.raw

    def dec(self, c: bytes, sk: bytes) -> bytes:
        """Given a Ntruprime secret key sk and a ciphertext c encapsulated to
        sk's corresponding public key pk, computes the session key k

        Example:
        >>> from pyntruprime import sntrup761
        >>> pk, sk = sntrup761.keypair()
        >>> c, k = sntrup761.enc(pk)
        >>> sntrup761.dec(c, sk) == k
        True
        """

        if not (isinstance(c, bytes) and isinstance(sk, bytes)):
            raise TypeError("c and sk must be bytes")
        if not len(c) == self._CIPHERTEXTBYTES:
            raise ValueError("c is wrong length")
        if not len(sk) == self._SECRETKEYBYTES:
            raise ValueError("sk is wrong length")

        c_arr = create_string_buffer(c)
        sk_arr = create_string_buffer(sk)
        k = create_string_buffer(self._BYTES)
        self._c_dec(k, c_arr, sk_arr)
        return k.raw


sntrup761 = _NTRU()
