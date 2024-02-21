import unittest
from rsa_crypto.rsa_crypto import RSAEncryption


class TestRSAEncryption(unittest.TestCase):
    def setUp(self):
        self.rsa = RSAEncryption()

    def test_encryption_decryption(self):
        original_text = 'Hello, this is a secret message!'
        encrypted_text = self.rsa.encrypt_with_public_key(original_text)
        decrypted_text = self.rsa.decrypt_with_private_key(encrypted_text)

        self.assertEqual(original_text, decrypted_text)


if __name__ == '__main__':
    unittest.main()
