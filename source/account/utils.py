# from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import PBKDF2PasswordHasher


def make_password_default(password: str):
    hasher = PBKDF2PasswordHasher()
    salt = hasher.salt()
    return hasher.encode(password, salt)
