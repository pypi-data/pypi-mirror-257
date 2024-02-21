from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class RSAEncryption:
    def __init__(self, env_file_path=None):
        # Set default paths relative to the script's location
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Load environment variables from the user's file if provided
        if env_file_path:
            env_file_path = os.path.abspath(env_file_path)
            load_dotenv(env_file_path)
        else:
            # If no specific file is provided, use the default .env file
            default_env_file_path = os.path.join(script_directory, '.env')
            load_dotenv(default_env_file_path)

        # Set the paths based on the loaded environment variables
        self.public_key_path = os.getenv('PUBLIC_KEY_PATH', os.path.join(script_directory, './keys/public_key.pem'))
        self.private_key_path = os.getenv('PRIVATE_KEY_PATH', os.path.join(script_directory, './keys/private_key.pem'))

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

    def encrypt_with_private_key(self, text):
        try:
            private_key = self._read_key(self.private_key_path)
            encrypted = private_key.sign(
                text.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(algorithm=padding.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            print(f"Encryption with private key failed: {e}")
            return None

    def decrypt_with_public_key(self, encrypted_text):
        try:
            public_key = self._read_key(self.public_key_path)
            encrypted_bytes = base64.b64decode(encrypted_text)
            public_key.verify(
                encrypted_bytes,
                text.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(algorithm=padding.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except cryptography.exceptions.InvalidSignature:
            return False
        except Exception as e:
            print(f"Decryption with public key failed: {e}")
            return None

    def _read_key(self, key_path):
        with open(key_path, 'rb') as key_file:
            key_data = key_file.read()
            return serialization.load_pem_private_key(key_data, password=None, backend=default_backend())
