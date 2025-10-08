import bcrypt
import db


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def register_user(username: str, password: str):
    hashed = hash_password(password)
    db.add_user(username, hashed)


def get_user(username: str):
    return db.get_user(username)
