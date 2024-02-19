# caesar_cipher.py

def shift_encrypt(message, shift):
    """
    Encrypts the given message using a Caesar cipher with the specified shift.

    Args:
        message (str): The message to be encrypted.
        shift (int): The shift value for the Caesar cipher.

    Returns:
        str: The encrypted message.
    """
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_message += chr(shifted)
        else:
            encrypted_message += char
    return encrypted_message

def shift_decrypt(encrypted_message, shift):
    """
    Decrypts the given encrypted message using a Caesar cipher with the specified shift.

    Args:
        encrypted_message (str): The encrypted message to be decrypted.
        shift (int): The shift value for the Caesar cipher.

    Returns:
        str: The decrypted message.
    """
    decrypted_message = ""
    for char in encrypted_message:
        if char.isalpha():
            shifted = ord(char) - shift
            if char.islower():
                if shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted < ord('A'):
                    shifted += 26
            decrypted_message += chr(shifted)
        else:
            decrypted_message += char
    return decrypted_message
