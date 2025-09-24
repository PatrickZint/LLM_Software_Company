'''Security module: Handles password hashing and note encryption/decryption using Fernet'''

import bcrypt
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from config import ENCRYPTION_ITERATIONS


def hash_password(password):
    '''Hashes a password and returns (hashed_password, salt)'''
    password_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return hash as string and salt as bytes
    return hashed.decode(), salt


def verify_password(password, hashed):
    '''Verifies a password against the stored hash'''
    return bcrypt.checkpw(password.encode(), hashed.encode())


def derive_key(password, salt):
    '''Derives a symmetric encryption key from the password and salt using PBKDF2HMAC'''
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ENCRYPTION_ITERATIONS,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt_note_content(content, key):
    '''Encrypts the note content using the provided key'''
    f = Fernet(key)
    return f.encrypt(content.encode())


def decrypt_note_content(token, key):
    '''Decrypts the note content token using the provided key'''
    f = Fernet(key)
    return f.decrypt(token).decode()
