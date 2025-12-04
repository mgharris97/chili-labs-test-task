# Hashing passwords
# Creation of JWT token

from passlib.context import CryptContext

# using bcrypt hashing algorithm 
# https://passlib.readthedocs.io/en/stable/lib/passlib.context.html
pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

# hash psswd
def hash_password(password: str):
    return pwd_context.hash(password)

# verify hashed psswd
def verify_password(plain: str, hashed: str):
    # verify(secret, hash,... **kwargs)
    return pwd_context.verify(plain, hashed)






