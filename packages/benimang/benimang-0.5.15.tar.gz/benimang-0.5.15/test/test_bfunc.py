import pytest

from beni.bfunc import (decrypt, decryptJson, decryptText, deobfuscate,
                        encrypt, encryptJson, encryptText, obfuscate)

_PASSWORD = 'test_password'
_DATA = '(故意地)混淆，使困惑，使模糊不清to make sth less clear and more difficult to understand, usually deliberately'.encode()


@pytest.mark.asyncio
async def test_obfuscate():
    magicContent = obfuscate(_DATA)
    assert deobfuscate(magicContent) == _DATA


@pytest.mark.asyncio
async def test_encrypt():
    data = encrypt(_DATA, _PASSWORD)
    assert decrypt(data, _PASSWORD) == _DATA


@pytest.mark.asyncio
async def test_encryptText():
    text = _DATA.decode()
    data = encryptText(text, _PASSWORD)
    assert decryptText(data, _PASSWORD) == text


@pytest.mark.asyncio
async def test_encryptJson():
    data = {'key': _DATA.decode()}
    text = encryptJson(data, _PASSWORD)
    assert decryptJson(text, _PASSWORD) == data
