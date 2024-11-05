import bcrypt


async def hash_password(password:str):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

async def check_password(hashed_password:str, plain_password:str):
    if not bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')):
        raise ValueError("Invalid credentials")