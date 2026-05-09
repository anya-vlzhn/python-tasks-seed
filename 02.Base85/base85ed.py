"""
Base85 encoder and decoder
"""

from __future__ import annotations
from beartype import beartype

a = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~"

@beartype
def encode(b: bytes):
    if len(b) == 0:
        return b""
    res = ""

    for i in range(0, len(b), 4):
        chunk = b[i:i+4]

        while len(chunk) < 4:
            chunk = chunk + b'\x00'

        n = (chunk[0] << 24) | (chunk[1] << 16) | (chunk[2] << 8) | chunk[3]

        ch = []
        for _ in range(5):
            ch.append(a[n % 85])
            n //= 85

        ch.reverse()
        enc = ''.join(ch)

        l = len(b[i:i + 4])
        res += enc[:l + 1]

    return res.encode('ascii')


@beartype
def decode(b: bytes):
    if len(b) == 0:
        return b""
    
    t = b.decode('ascii')

    while len(t) % 5 != 0:
        t += '~'

    res = bytearray()

    for i in range(0, len(t), 5):
        bl = t[i:i + 5]

        n = 0
        for char in bl:
            n = n * 85 + a.index(char)
        
        res.append((n >> 24) & 0xFF)
        res.append((n >> 16) & 0xFF)
        res.append((n >> 8) & 0xFF)
        res.append(n & 0xFF)

        byt = (len(b) * 4) // 5
    return bytes(res[:byt])
