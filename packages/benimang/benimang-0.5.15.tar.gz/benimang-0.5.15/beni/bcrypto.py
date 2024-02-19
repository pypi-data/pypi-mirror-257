# import base64
# import os

# from cryptography.fernet import Fernet
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# def encode(content: str, password: str) -> str:
#     '使用密码加密信息'
#     salt = os.urandom(16)  # 生成盐
#     key = _genKey(password, salt)  # 根据密码和盐生成密钥
#     fernet = Fernet(key)
#     magicContent = fernet.encrypt(content.encode())
#     return _mergeSalt(magicContent.decode(), salt.hex())


# def decode(magicContent: str, password: str) -> str:
#     '使用密码解密信息'
#     magicContent, salt = _splitSalt(magicContent)
#     key = _genKey(password, bytes.fromhex(salt))
#     fernet = Fernet(key)
#     return fernet.decrypt(magicContent).decode()


# def _genKey(password: str, salt: bytes) -> bytes:
#     '根据给定的密码和盐值生成密钥'
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=32,
#         salt=salt,
#         iterations=100000,
#         backend=default_backend()
#     )
#     return base64.urlsafe_b64encode(kdf.derive(password.encode()))


# _LIST_SIZE = 8


# def _mergeSalt(magicContent: str, salt: str) -> str:
#     '将盐值合并到加密后的内容中'
#     num = len(magicContent)
#     assert num > _LIST_SIZE ** 2, '生成的密文不支持小于100个字符'
#     offset = num % _LIST_SIZE
#     size = num // _LIST_SIZE - offset
#     magicContentList = _strToList(magicContent, _LIST_SIZE, size)
#     saltList = _strToList(salt, _LIST_SIZE, size)
#     return _mergeTwoList(magicContentList, saltList)


# def _splitSalt(magicContent: str) -> tuple[str, str]:
#     '从加密后的内容中分离出盐值'
#     num = len(magicContent) - 32
#     offset = num % _LIST_SIZE
#     size = num // _LIST_SIZE - offset
    
#     salt, magicContent = magicContent.split(' ', 1)
#     return magicContent, salt


# def _strToList(text: str, num_elements: int, element_size: int) -> list[str]:
#     result = []
#     start = 0
#     for _ in range(num_elements - 1):
#         result.append(text[start:start + element_size])
#         start += element_size
#     result.append(text[start:])
#     return result


# def _mergeTwoList(aa: list[str], bb: list[str]) -> str:
#     ary: list[str] = []
#     for a, b in zip(aa, bb):
#         ary.append(a)
#         ary.append(b)
#     return ''.join(ary)
