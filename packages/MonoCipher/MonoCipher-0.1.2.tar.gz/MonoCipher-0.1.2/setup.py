from setuptools import setup, find_packages
from setuptools.command.install import install
from tqdm import tqdm
import time

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Custom install command that shows progress using tqdm
class CustomInstallCommand(install):
    def run(self):
        # Call the parent class method
        install.run(self)
        
        # Simulate installation progress with tqdm
        for i in tqdm(range(100)):
            time.sleep(0.1)

setup(
    name='MonoCipher',
    version='0.1.2',
    description='A package for monoalphabetic ciphers (message encryption and decryption).',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/rakeshkanna-rk/MonoCipher',
    author='Rakesh Kanna',
    license='MIT',
    author_email='rakeshkanna0108@gmail.com',
    project_urls={
        'GitHub': 'https://github.com/rakeshkanna-rk/MonoCipher/',
        'PyPI' : 'https://pypi.org/project/MonoCipher/'
    },
    packages=find_packages(),
    install_requires=[
        "pycryptodome>=3.20.0",
        'tqdm'
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ShiftEncrypt = MonoCipher.SimpleEncryption:shift_encrypt',
            'ShiftDecrypt = MonoCipher.SimpleEncryption:shift_decrypt',
            'ByteEncrypt = MonoCipher.ByteEncryption:byte_encrypt',
            'ByteDecrypt = MonoCipher.ByteEncryption:byte_decrypt',
            'SaltEncrypt = MonoCipher.SaltEncryption:salt_encrypt',
            'SaltDecrypt = MonoCipher.SaltEncryption:salt_decrypt',
        ]
    }
)
