import unittest

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from src.metrics import percent_change, standard_error
from src.problem import PAYLOAD_SIZES, PLATFORMS, REQUIRED_ALGORITHMS
from src.secure_channel import (
    SecureChannelError, _tamper_check, derive_aes_key, oqs,
)


class ProjectTests(unittest.TestCase):
    def test_online_scope_is_only_platform_a_and_b(self):
        self.assertEqual(set(PLATFORMS), {"A", "B"})

    def test_required_algorithms_are_declared(self):
        self.assertEqual(REQUIRED_ALGORITHMS["key_establishment"], "ML-KEM-768 (NIST FIPS 203)")
        self.assertEqual(REQUIRED_ALGORITHMS["authentication"], "ML-DSA-65 (NIST FIPS 204)")
        self.assertEqual(REQUIRED_ALGORITHMS["key_derivation"], "HKDF-SHA-256")
        self.assertEqual(REQUIRED_ALGORITHMS["payload_encryption"], "AES-256-GCM")

    def test_payload_sizes(self):
        self.assertEqual(PAYLOAD_SIZES, {"1KB": 1024, "100KB": 102400, "10MB": 10485760})

    def test_hkdf_key_and_aes_gcm_tamper_rejection(self):
        key = derive_aes_key(b"test shared secret", b"test context")
        self.assertEqual(len(key), 32)
        nonce = b"\x00" * 12
        aad = b"test aad"
        encrypted = AESGCM(key).encrypt(nonce, b"hello", aad)
        self.assertEqual(AESGCM(key).decrypt(nonce, encrypted, aad), b"hello")
        self.assertTrue(_tamper_check(key, nonce, encrypted, aad))

    def test_standard_error(self):
        self.assertAlmostEqual(standard_error([1, 2, 3]), 0.577350269, places=6)
        self.assertEqual(standard_error([2]), 0.0)

    def test_percent_change(self):
        self.assertEqual(percent_change(10, 12), 20.0)
        with self.assertRaises(ValueError):
            percent_change(0, 1)

    @unittest.skipIf(oqs is None, "liboqs-python/native liboqs not installed; integration test skipped")
    def test_full_pqc_handshake_round_trip(self):
        from src.secure_channel import demo_round_trip
        result = demo_round_trip("test message")
        self.assertTrue(result["correct"])
        self.assertTrue(result["tamper_rejected"])
        self.assertEqual(result["decrypted_text"], "test message")


if __name__ == "__main__":
    unittest.main()
