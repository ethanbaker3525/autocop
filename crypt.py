import base64
import os
from argon2                                    import PasswordHasher
from cryptography.fernet                       import Fernet
from cryptography.hazmat.backends              import default_backend
from cryptography.hazmat.primitives            import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Encryption:

    def __init__(self, data, password):
        self.salt = os.urandom(16)
        self.token = Fernet(base64.urlsafe_b64encode(PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=self.salt,iterations=100000,backend=default_backend()).derive(password))).encrypt(data)
        self.hash = PasswordHasher().hash(password)

    def __str__(self):
        return self.token.decode('utf-8')

    def decrypt(self, password):
        assert PasswordHasher().verify(self.hash, password), 'password does not match hash'
        return Fernet(base64.urlsafe_b64encode(PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=self.salt,iterations=100000,backend=default_backend()).derive(password))).decrypt(self.token)
