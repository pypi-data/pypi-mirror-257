# aes_cipher.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def byte_encrypt(message, keys):
    """
    Encrypts the given message using AES encryption in CBC mode.

    Args:
        message (str): The message to be encrypted.
        key (bytes): The encryption key.

    Returns:
        tuple: A tuple containing the initialization vector (iv) and the ciphertext.
    """
    key = bytes(keys, encoding="utf-8")
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return iv, ciphertext

def byte_decrypt(iv, ciphertext, password):
    """
    Decrypts the given ciphertext using AES encryption in CBC mode.

    Args:
        iv (str): The initialization vector.
        ciphertext (str): The ciphertext.
        password (str): The decryption password.

    Returns:
        str: The decrypted message.
    """
    
    key = password.encode('utf-8')
    iv = base64.b64decode(iv)
    ciphertext = base64.b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode('utf-8')