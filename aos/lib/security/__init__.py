import base64
from aos.lib.common_utils import pyDes

_crypter = None
_crypt_secret = 'kit-aos!' #must be exactly 8 chars long
def encrypt(str):
    global _crypter
    if not _crypter:
        _crypter = pyDes.des(_crypt_secret)
    return base64.b16encode(_crypter.encrypt(str, padmode=pyDes.PAD_PKCS5))

def decrypt(str):
    global _crypter
    if not _crypter:
        _crypter = pyDes.des(_crypt_secret)
    return _crypter.decrypt(base64.b16decode(str), padmode=pyDes.PAD_PKCS5)  