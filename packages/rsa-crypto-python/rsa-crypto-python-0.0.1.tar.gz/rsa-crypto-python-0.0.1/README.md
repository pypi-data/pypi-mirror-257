# RSA Encryption Python Package

A Python package for asymmetric encryption using RSA.

## Installation

```bash
pip install rsa-crypto-python
```

## Usage

```python
from rsa-crypto-python.rsa_crypto import RSAEncryption

# Create an instance of the RSAEncryption class
rsa = RSAEncryption()

# Encrypt with public key
original_text = 'Hello, this is a secret message!'
encrypted_text = rsa.encrypt_with_public_key(original_text)
print('Encrypted Text:', encrypted_text)

# Decrypt with private key
decrypted_text = rsa.decrypt_with_private_key(encrypted_text)
print('Decrypted Text:', decrypted_text)
```

## Configuration
Set your public and private key paths in a .env file:
```bash
PUBLIC_KEY  = "-----BEGIN PUBLIC KEY-----
YOUR_PUBLIC_KEY_HERE
-----END PUBLIC KEY-----"


PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_HERE
-----END PRIVATE KEY-----"
```

### To generate keys
Generate Private Key
```bash
openssl genpkey -algorithm RSA
```

Generate Public Key
```bash
openssl rsa -pubout -in <(openssl genpkey -algorithm RSA)
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
