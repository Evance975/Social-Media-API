from passlib.context import CryptContext

#bcrypt is the default hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

#the following function takes a raw password, hash it and compare it to the hashed password in the db
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)