import binascii
import hashlib


def hash_simple(key: bytes, string: str, algorithm: str = 'sha512', length: int = 20):
    cipher = int(binascii.hexlify(hashlib.pbkdf2_hmac(algorithm, string, key, 100000)), 16) % (10 ** length)
    return cipher
