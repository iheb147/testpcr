```python
import hashlib
import hmac
import secrets
from typing import Optional

ITERATIONS = 100000

# Use a proper password hashing library (bcrypt) for production.
# For this example, we use hashlib.pbkdf2_hmac with a salt.
def _hash_password(password: str, salt: bytes = None) -> tuple:
    if salt is None:
        salt