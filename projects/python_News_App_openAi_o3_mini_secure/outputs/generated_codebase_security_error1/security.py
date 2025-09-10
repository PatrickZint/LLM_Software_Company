from cryptography.fernet import Fernet


# For simplicity, we use Fernet for symmetric encryption which internally uses AES-256.
# In a production environment, key management must be performed securely.

# In a real application, the key should not be hard-coded,
# but for demonstration purposes we use a fixed key here.
KEY = b'_A1b2C3d4E5f6G7h8I9j0K1L2M3N4O5P6'

cipher_suite = Fernet(KEY)


def encrypt(plaintext):
    """Encrypt plaintext (string) using Fernet symmetric encryption."""
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    encrypted_text = cipher_suite.encrypt(plaintext)
    return encrypted_text.decode('utf-8')


def decrypt(ciphertext):
    """Decrypt ciphertext (string) using Fernet symmetric encryption."""
    decrypted_text = cipher_suite.decrypt(ciphertext.encode('utf-8'))
    return decrypted_text.decode('utf-8')
