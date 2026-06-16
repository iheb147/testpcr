import hashlib
import hmac
import secrets
from typing import Optional, Tuple

ITERATIONS = 600000

def _hash_password(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
    if salt is None:
        salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, ITERATIONS)
    return dk, salt