import base64
import json
import uuid
from typing import Any

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from beni.bfunc import deobfuscate, jsonDumpsMini, obfuscate


def _getEncryptKey(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt(data: bytes, password: str) -> bytes:
    '加密内容'
    salt = uuid.uuid4().hex.encode()
    key = _getEncryptKey(password, salt)
    fernet = Fernet(key)
    result = fernet.encrypt(data)
    result = obfuscate(result + salt)
    return result


def encryptText(text: str, password: str) -> bytes:
    return encrypt(text.encode(), password)


def encryptJson(data: Any, password: str) -> bytes:
    return encrypt(jsonDumpsMini(data).encode(), password)


def decrypt(data: bytes, password: str) -> bytes:
    '解密内容'
    data = data.split(b' ')[-1]
    data = deobfuscate(data)
    salt = data[-32:]
    data = data[:-32]
    key = _getEncryptKey(password, salt)
    fernet = Fernet(key)
    return fernet.decrypt(data)


def decryptText(data: bytes, password: str) -> str:
    return decrypt(data, password).decode()


def decryptJson(data: bytes, password: str) -> Any:
    return json.loads(decrypt(data, password).decode())
