# utils/security.py

import random
import string
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generate_unique_code(prefix: str = "MDG", length: int = 7) -> str:
    """
    Génère un code unique du type MDG2024001
    """
    suffix = "".join(random.choices(string.digits, k=length))
    return f"{prefix}{suffix}"
