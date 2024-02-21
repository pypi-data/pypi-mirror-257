import unittest
from rsa_crypto_python.rsa_crypto_python import RSAEncryption


class TestRSAEncryption(unittest.TestCase):
    def setUp(self):
        self.rsa = RSAEncryption()

    def test_encryption_decryption_public_to_private(self):
        original_text = 'Hello, this is a secret message! public_to_private'
        encrypted_text = self.rsa.encrypt_with_public_key(original_text)
        decrypted_text = self.rsa.decrypt_with_private_key(encrypted_text)

        self.assertEqual(original_text, decrypted_text)

    def test_encryption_decryption_private_to_public(self):
        original_text = 'Hello, this is a secret message! private_to_public'
        encrypted_text = self.rsa.encrypt_with_private_key(original_text)
        decrypted_text = self.rsa.decrypt_with_public_key(encrypted_text)

        self.assertEqual(original_text, decrypted_text)


if __name__ == '__main__':
    unittest.main()
