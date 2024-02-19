from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='MonoCipher',
    version='0.1.0',
    description='A package for monoalphabetic ciphers (encryption and decryption).',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/rakeshkanna-rk/MonoCipher',
    author='Rakesh Kanna',
    author_email='rakeshkanna0108@gmail.com',
    packages=find_packages(),
    install_requires=[
        "pycryptodome>=3.20.0"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'mono-shift-encrypt = MonoCipher.SimpleEncryption:shift_encrypt',
            'mono-byte-encrypt = MonoCipher.ByteEncryption:byte_encrypt',
            'mono-salt-encrypt = MonoCipher.SaltEncryption:salt_encrypt',
        ]
    }
)
