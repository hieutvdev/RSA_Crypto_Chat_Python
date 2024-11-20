import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(input_password: str, stored_hash: str) -> bool:
    input_hash = hash_password(input_password)
    return input_hash == stored_hash

