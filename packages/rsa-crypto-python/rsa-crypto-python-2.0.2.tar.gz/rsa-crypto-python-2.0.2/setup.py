from setuptools import setup, find_packages

setup(
    name='rsa-crypto-python',
    version='2.0.2',
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'python-dotenv'
    ],
    test_suite='tests',
)
