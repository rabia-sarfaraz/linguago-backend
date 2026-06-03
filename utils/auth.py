import bcrypt


def hash_password(password: str) -> str:
    """Plain password ko hash karta hai (secure storage)"""
    # bcrypt ki 72-byte limit handle karne ke liye encode + truncate
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Login ke time password check karta hai"""
    pwd_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)