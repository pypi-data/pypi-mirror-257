"""This module provides functions to encrypt and decrypt data.
"""

import sys
import platform
import hashlib
from collections import namedtuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import base64
from urllib.parse import quote, unquote
from typing import AnyStr
from pycinante.reflect import cinvoke

__all__ = [
    'md5',
    'sha1',
    'sha256',
    'sha512',
    'blake2',
    'shake128',
    'shake256',
    'fernet_key',
    'fernet_encrypt',
    'fernet_decrypt',
    'rsa_key',
    'RSAKey',
    'rsa_encrypt',
    'rsa_decrypt',
    'rsa_sign',
    'rsa_verify',
    'base64_encode',
    'base64_decode',
    'url_encode',
    'url_decode'
]

RSAKey = namedtuple('RSAKey', ['public', 'private'])

def md5(s: str, encoding: str = None) -> str:
    """Return the md5 hex digest of the given string.

    >>> md5('hello world')
    '5eb63bbbe01eeed093cb22bb8f5acdc3'
    """
    s = s.encode(encoding or sys.getdefaultencoding())
    return hashlib.md5(s).hexdigest()

def sha1(s: str, encoding: str = None) -> str:
    """Return the sh1 hex digest of the given string.

    >>> sha1('hello world')
    '2aae6c35c94fcfb415dbe95f408b9ce91ee846ed'
    """
    s = s.encode(encoding or sys.getdefaultencoding())
    return hashlib.sha1(s).hexdigest()

def sha256(s: str, encoding: str = None) -> str:
    """Return the sh256 hex digest of the given string.

    >>> sha256('hello world')
    'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
    """
    s = s.encode(encoding or sys.getdefaultencoding())
    return hashlib.sha256(s).hexdigest()

def sha512(s: str, encoding: str = None) -> str:
    """Return the sh512 hex digest of the given string.

    >>> sha512('hello world')[:64]
    '309ecc489c12d6eb4cc40f50c902f2b4d0ed77ee511a7c7a9bcd3ca86d4cd86f'
    """
    s = s.encode(encoding or sys.getdefaultencoding())
    return hashlib.sha512(s).hexdigest()

def blake2(s: str, encoding: str = None, **kwargs) -> str:
    """Return the Blake2 hex digest of the given string.

    >>> blake2('hello world')[:64]
    '021ced8799296ceca557832ab941a50b4a11f83478cf141f51f933f653ab9fbc'
    """
    is_64bits = platform.architecture()[0].startswith('64')
    digest_size = kwargs.pop('digest_size', (is_64bits and 64) or 32)
    blake2 = ((is_64bits and hashlib.blake2b) or hashlib.blake2s)
    s = s.encode(encoding or sys.getdefaultencoding())
    return blake2(s, digest_size=digest_size, **kwargs).hexdigest()

def shake128(s: str, encoding: str = None) -> str:
    """Return the shake 128 hex digest of the given string.

    >>> shake128('hello world')[:64]
    '3a9159f071e4dd1c8c4f968607c30942e120d8156b8b1e72e0d376e8871cb8b8'
    """
    return hashlib.shake_128(s.encode(encoding or sys.getdefaultencoding())).hexdigest(64)

def shake256(s: str, encoding: str = None) -> str:
    """Return the shake 256 hex digest of the given string.

    >>> shake256('hello world')[:64]
    '369771bb2cb9d2b04c1d54cca487e372d9f187f73f7ba3f65b95c8ee7798c527'
    """
    return hashlib.shake_256(s.encode(encoding or sys.getdefaultencoding())).hexdigest(64)

def fernet_key(decoding: str = None) -> AnyStr:
    """Return a fernet key decoded by the given `decoding`.

    >>> assert fernet_key()
    """
    return cinvoke(decoding, Fernet.generate_key(), 'decode', decoding)

def fernet_encrypt(s: AnyStr, key: AnyStr, encoding: str = None, decoding: str = None) -> AnyStr:
    """Return the ciphertext encrypted with the given fernet key.

    >>> assert fernet_encrypt('hello world', fernet_key())
    """
    encoding = encoding or sys.getdefaultencoding()
    s = Fernet(key).encrypt(isinstance(s, str) and s.encode(encoding) or s)
    return cinvoke(decoding, s, 'decode', decoding)

def fernet_decrypt(s: AnyStr, key: AnyStr, decoding: str = None) -> AnyStr:
    """Return the plaintext decrypted with the given fernet key.

    >>> key = fernet_key()
    >>> fernet_decrypt(fernet_encrypt('hello world', key), key, 'utf-8')
    'hello world'
    """
    return cinvoke(decoding, Fernet(key).decrypt(s), 'decode', decoding)

def rsa_key(decoding: str = None, **kwargs) -> RSAKey:
    """Return a RAS key decoded by the given `decoding`.

    >>> key = rsa_key()
    >>> assert key.public and key.private
    """
    private_key = rsa.generate_private_key(
        public_exponent=kwargs.pop('public_exponent', 65537),
        key_size=kwargs.pop('key_size', 2048),
        backend=kwargs.pop('backend', default_backend()))
    public_key = private_key.public_key()
    private_key = cinvoke(decoding, private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ), 'decode', decoding)
    public_key = cinvoke(decoding, public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ), 'decode', decoding)
    return RSAKey(public=public_key, private=private_key)

def rsa_encrypt(s: AnyStr, key: AnyStr, encoding: str = None, decoding: str = None) -> AnyStr:
    """Return the ciphertext encrypted with the given public key.

    >>> assert rsa_encrypt('hello world', rsa_key().public)
    """
    encoding = encoding or sys.getdefaultencoding()
    key = (isinstance(key, str) and key.encode(encoding)) or key
    encipher = serialization.load_pem_public_key(key, default_backend())
    s = encipher.encrypt(isinstance(s, str) and s.encode(encoding) or s, padding.OAEP(
        padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
    return cinvoke(decoding, s, 'decode', decoding)

def rsa_decrypt(s: AnyStr, key: AnyStr, password: bytes = None, encoding: str = None, decoding: str = None) -> AnyStr:
    """Return the plaintext decrypted with the given private key.

    >>> key = rsa_key()
    >>> rsa_decrypt(rsa_encrypt('hello world', key.public), key.private, decoding='utf-8')
    'hello world'
    """
    encoding = encoding or sys.getdefaultencoding()
    key = (isinstance(key, str) and key.encode(encoding)) or key
    decipher = serialization.load_pem_private_key(key, password, default_backend())
    s = decipher.decrypt(isinstance(s, str) and s.encode(encoding) or s, padding.OAEP(
        padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
    return cinvoke(decoding, s, 'decode', decoding)

def rsa_sign(s: AnyStr, key: AnyStr, password: bytes = None, encoding: str = None) -> AnyStr:
    """Sign a raw sequence using the given private key.

    >>> assert rsa_sign('hello world', rsa_key().private)
    """
    encoding = encoding or sys.getdefaultencoding()
    key = (isinstance(key, str) and key.encode(encoding)) or key
    signer = serialization.load_pem_private_key(key, password, default_backend())
    s = isinstance(s, str) and s.encode(encoding) or s
    return signer.sign(s, padding=padding.PSS(
        padding.MGF1(hashes.SHA256()),
        padding.PSS.MAX_LENGTH), algorithm=hashes.SHA256())

# noinspection PyBroadException
def rsa_verify(s: AnyStr, signature: AnyStr, key: AnyStr, encoding: str = None) -> bool:
    """Verifies the signature of the data using the given public key.

    >>> key = rsa_key()
    >>> rsa_verify('hello world', rsa_sign('hello world', key.private), key.public)
    True
    """
    encoding = encoding or sys.getdefaultencoding()
    key = (isinstance(key, str) and key.encode(encoding)) or key
    verifier = serialization.load_pem_public_key(key, default_backend())
    try:
        s = isinstance(s, str) and s.encode(encoding) or s
        signature = (isinstance(signature, str) and signature.encode(encoding)) or signature
        verifier.verify(signature, s, padding=padding.PSS(
            padding.MGF1(hashes.SHA256()),
            padding.PSS.MAX_LENGTH), algorithm=hashes.SHA256())
        return True
    except Exception:
        return False

def base64_encode(s: AnyStr, encoding: str = None, decoding: str = None) -> AnyStr:
    """Encode bytes using the URL- and filesystem-safe Base64 alphabet.

    >>> base64_encode('hello world', decoding='utf-8')
    'aGVsbG8gd29ybGQ='
    """
    encoding = encoding or sys.getdefaultencoding()
    s = base64.urlsafe_b64encode(isinstance(s, str) and s.encode(encoding) or s)
    return cinvoke(decoding, s, 'decode', decoding)

def base64_decode(s: AnyStr, encoding: str = None, decoding: str = None) -> AnyStr:
    """Decode bytes using the URL- and filesystem-safe Base64 alphabet.

    >>> base64_decode('aGVsbG8gd29ybGQ=', decoding='utf-8')
    'hello world'
    """
    encoding = encoding or sys.getdefaultencoding()
    s = base64.urlsafe_b64decode(isinstance(s, str) and s.encode(encoding) or s)
    return cinvoke(decoding, s, 'decode', decoding)

def url_encode(s: AnyStr, encoding: str = None, **kwargs) -> str:
    """Encode bytes or string based on Uniform Resource Identifier (URI).

    >>> url_encode('q=how to say 你好 in English ?')
    'q%3Dhow%20to%20say%20%E4%BD%A0%E5%A5%BD%20in%20English%20%3F'
    """
    return quote(s, encoding=encoding, **kwargs)

def url_decode(s: AnyStr, encoding: str = None, **kwargs) -> str:
    """Decode bytes or string based on Uniform Resource Identifier (URI).

    >>> url_decode('q%3Dhow%20to%20say%20%E4%BD%A0%E5%A5%BD%20in%20English%20%3F')
    'q=how to say 你好 in English ?'
    """
    return unquote(s, encoding=encoding, **kwargs)
