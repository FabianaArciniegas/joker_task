import bcrypt


async def hash_password(password: str):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


async def check_password(hashed_password: str, plain_password: str) -> None:
    if not bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')):
        raise ValueError("Invalid credentials")


async def verified_user_confirmation(is_verified: bool) -> None:
    if not is_verified:
        raise ValueError("User not verified")
