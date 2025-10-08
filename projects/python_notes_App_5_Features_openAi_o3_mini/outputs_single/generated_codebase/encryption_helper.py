import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


def generate_salt():
    return os.urandom(16)


def derive_key(password, salt):
    # Derive a 32-byte key from the password and salt using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def encrypt_text(key, text):
    f = Fernet(key)
    return f.encrypt(text.encode('utf-8'))


def decrypt_text(key, token):
    f = Fernet(key)
    return f.decrypt(token).decode('utf-8')
