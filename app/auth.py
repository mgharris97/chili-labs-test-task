# Hashing passwords
# Creation of JWT token

from passlib.context import CryptContext

# using bcrypt hashing algorithm 
# https://passlib.readthedocs.io/en/stable/lib/passlib.context.html
pwd_context = CryptContext(schemes=["bcrypt"], Deprecated = "auto")

# hash psswd
def hash_password(password: str):
    return pwd_context.hash(password)

# 
def verify_password(plain: str, hashed: str):
    # verify(secret, hash,... **kwargs)
    return pwd_context.verify(plain, hashed)



