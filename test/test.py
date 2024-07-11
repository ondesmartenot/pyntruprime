from unittest import TestCase, main

from pyntruprime import sntrup761


class TestNTRUPrime(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_all(self) -> None:
        kems = [sntrup761]

        for kem in kems:
            print(f"{kem._PARAMS}...", end="")
            pk, sk = kem.keypair()
            c, k = kem.enc(pk)
            self.assertEqual(kem.dec(c, sk), k)
            print("Good")


if __name__ == "__main__":
    main()
