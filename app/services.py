import hashlib
import base64

def create_hashed_url(original_url: str, length: int = 8):

    hash = hashlib.md5(original_url.encode())
    hash_bytes = hash.digest()
    base64_hash = base64.urlsafe_b64encode(hash_bytes).decode()
    key = base64_hash[:length]

    
    return key