import os
import hashlib
import hmac
import base64
import json
import time
from datetime import datetime, timedelta
from typing import Optional, Any, Union
from app.core.config import settings

try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False

def get_password_hash(password: str) -> str:
    """Secure password hashing with salt using bcrypt or PBKDF2-HMAC-SHA256."""
    if HAS_BCRYPT:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')
    else:
        salt = os.urandom(16)
        kdf = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return "pbkdf2$" + base64.b64encode(salt).decode('ascii') + "$" + base64.b64encode(kdf).decode('ascii')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify hashed password safely against timing attacks."""
    if not hashed_password or not plain_password:
        return False
    if hashed_password.startswith("$2b$") or hashed_password.startswith("$2a$"):
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False
    elif hashed_password.startswith("pbkdf2$"):
        try:
            _, salt_b64, hash_b64 = hashed_password.split("$")
            salt = base64.b64decode(salt_b64.encode('ascii'))
            expected_hash = base64.b64decode(hash_b64.encode('ascii'))
            actual_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
            return hmac.compare_digest(actual_hash, expected_hash)
        except Exception:
            return False
    return False

def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('ascii').rstrip('=')

def _base64url_decode(data: str) -> bytes:
    padding = '=' * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode((data + padding).encode('ascii'))

def create_access_token(subject: Union[str, Any], role: str = "USER", expires_delta: Optional[timedelta] = None) -> str:
    """Create a standardized secure JWT access token without external library fragility."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": str(subject),
        "role": role,
        "exp": int(expire.timestamp()),
        "iat": int(time.time())
    }
    
    encoded_header = _base64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    encoded_payload = _base64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
    
    signature_input = f"{encoded_header}.{encoded_payload}".encode('ascii')
    signature = hmac.new(settings.SECRET_KEY.encode('utf-8'), signature_input, hashlib.sha256).digest()
    encoded_signature = _base64url_encode(signature)
    
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

def decode_token(token: str) -> Optional[dict]:
    """Decode and cryptographically verify JWT token."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        encoded_header, encoded_payload, encoded_signature = parts
        
        signature_input = f"{encoded_header}.{encoded_payload}".encode('ascii')
        expected_sig = hmac.new(settings.SECRET_KEY.encode('utf-8'), signature_input, hashlib.sha256).digest()
        actual_sig = _base64url_decode(encoded_signature)
        
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None
            
        payload = json.loads(_base64url_decode(encoded_payload).decode('utf-8'))
        
        # Check expiration
        if "exp" in payload and payload["exp"] < int(time.time()):
            return None
            
        return payload
    except Exception:
        return None
