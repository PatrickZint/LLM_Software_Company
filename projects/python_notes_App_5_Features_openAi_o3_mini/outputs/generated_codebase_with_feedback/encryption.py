import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# In a production system, use a unique salt per user and store it securely.
# For this MVP, we use a constant salt.
SALT = b'static_salt_12345'


def derive_key(password: str) -> bytes:
    password_bytes = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key


def encrypt_data(key: bytes, data: str) -> bytes:
    f = Fernet(key)
    token = f.encrypt(data.encode())
    return token


def decrypt_data(key: bytes, token: bytes) -> str:
    f = Fernet(key)
    data = f.decrypt(token)
    return data.decode()
