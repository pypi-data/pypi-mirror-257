from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class RSAEncryption:
    def __init__(self):
        self.public_key_path = os.getenv('PUBLIC_KEY', '../keys/public_key.pem')
        self.private_key_path = os.getenv('PRIVATE_KEY', '../keys/private_key.pem')

    def encrypt_with_public_key(self, text):
        public_key = self._read_key(self.public_key_path)
        encrypted = public_key.encrypt(
            text.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=padding.SHA256()),
                algorithm=padding.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt_with_private_key(self, encrypted_text):
        private_key = self._read_key(self.private_key_path)
        encrypted_bytes = base64.b64decode(encrypted_text)
        decrypted = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=padding.SHA256()),
                algorithm=padding.SHA256(),
                label=None
            )
        )
        return decrypted.decode('utf-8')

    def _read_key(self, key_path):
        with open(key_path, 'rb') as key_file:
            key_data = key_file.read()
            return serialization.load_pem_private_key(key_data, password=None, backend=default_backend())
