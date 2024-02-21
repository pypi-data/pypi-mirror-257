# RSA Encryption Python Package

A Python package for asymmetric encryption using RSA.

## Installation

```bash
pip install rsa-crypto-python
```

## Usage

```python
from rsa_crypto_python.rsa_crypto_python import RSAEncryption

# Create an instance of the RSAEncryption class

rsa = RSAEncryption()
# rsa = RSAEncryption(env_file_path=None)


# crypt private_to_public
original_text = 'Hello, this is a secret message!'
encrypted_text = rsa.encrypt_with_private_key(original_text)
print('Encrypted Text:', encrypted_text)


decrypted_text = rsa.decrypt_with_public_key(encrypted_text)
print('Decrypted Text:', decrypted_text)

# crypt public_to_private
original_text = 'Hello, this is a secret message!'
encrypted_text = rsa.encrypt_with_public_key(original_text)
print('Encrypted Text:', encrypted_text)


decrypted_text = rsa.decrypt_with_private_key(encrypted_text)
print('Decrypted Text:', decrypted_text)
```

## Configuration
Set your public and private key paths in a .env file:
```bash
PUBLIC_KEY_PATH=/path/to/your/keys/public_key.pem
PRIVATE_KEY_PATH=/path/to/your/keys/private_key.pem
```

### To generate keys
Generate Private Key
```bash
openssl genpkey -algorithm RSA -out keys/private_key.pem
```

Generate Public Key
```bash
openssl rsa -pubout -in keys/private_key.pem -out keys/public_key.pem
```


## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -am 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the cryptography library for providing the tools for secure communication.

## Author

Ukweh Everest

## Contact

For any inquiries, please contact [exrelativity@gmail.com].
