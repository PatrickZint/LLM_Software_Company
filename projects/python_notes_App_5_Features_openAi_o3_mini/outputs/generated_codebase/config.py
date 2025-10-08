'''Configuration module for the Secure Note-Taking Application'''

# Database configuration
DB_PATH = "notes.db"

# Encryption configuration
# Number of iterations for key derivation (PBKDF2)
ENCRYPTION_ITERATIONS = 100000

# Salt size in bytes
SALT_SIZE = 16
