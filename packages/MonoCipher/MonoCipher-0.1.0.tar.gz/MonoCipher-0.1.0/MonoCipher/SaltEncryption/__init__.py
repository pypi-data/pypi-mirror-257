# salt_cipher.py
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def generate_key(password, salt):
    """
    Generates a key using PBKDF2 key derivation function.

    Args:
        password (str): The password.
        salt (bytes): The salt value.

    Returns:
        bytes: The generated key.
    """
    key = PBKDF2(password, salt, dkLen=32)  # 256-bit key
    return key

def salt_encrypt(message, password):
    """
    Encrypts the given message using AES encryption in CBC mode with salt.

    Args:
        message (str): The message to be encrypted.
        password (str): The password.

    Returns:
        tuple: A tuple containing the salt, initialization vector (iv), and the ciphertext.
    """
    salt = get_random_bytes(16)
    key = generate_key(password, salt)
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    salt = base64.b64encode(salt).decode('utf-8')
    return salt, iv, ciphertext

def salt_decrypt(salt, iv, ciphertext, password):
    """
    Decrypts the given ciphertext using AES encryption in CBC mode with salt.

    Args:
        salt (str): The base64-encoded salt.
        iv (str): The base64-encoded initialization vector.
        ciphertext (str): The base64-encoded ciphertext.
        password (str): The password.

    Returns:
        str: The decrypted message.
    """
    salt = base64.b64decode(salt)
    key = generate_key(password, salt)
    iv = base64.b64decode(iv)
    ciphertext = base64.b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode('utf-8')
