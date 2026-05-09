"""
Unit tests for 02.Base85
"""

import base85ed


def test_shorts_encode():
    """
    Test trivial short encodes
    """
    assert base85ed.encode(b"1") == b"F#"
    assert base85ed.encode(b"12") == b"F){"
    assert base85ed.encode(b"123") == b"F)}j"
    assert base85ed.encode(b"1234") == b"F)}kW"


def test_shorts_decode():
    """
    Test trivial short decodes
    """
    assert base85ed.decode(b"F#") == b"1"
    assert base85ed.decode(b"F){") == b"12"
    assert base85ed.decode(b"F)}j") == b"123"
    assert base85ed.decode(b"F)}kW") == b"1234"


def test_empty():
    """
    Test empty string
    """
    assert base85ed.encode(b"") == b""
    assert base85ed.decode(b"") == b""


def test_all_bytes():
    """
    All 256 byte values must survive encode/decode
    """
    data = bytes(range(256))
    enc = base85ed.encode(data)
    dec = base85ed.decode(enc)
    assert dec == data


def test_bit_patterns():
    """
    Test critical bit patterns
    """
    for data in [b"\x00\x00\x00\x00", b"\xff\xff\xff\xff", b"\x00\x00\x00\x01", b"\x80\x00\x00\x00"]:
        enc = base85ed.encode(data)
        dec = base85ed.decode(enc)
        assert dec == data


def test_boundary_len():
    """
    Test crossing block boundary: 1, 2, 3, 4, 5 bytes
    """
    for l in [1, 2, 3, 4, 5]:
        data = bytes(range(l))
        enc = base85ed.encode(data)
        dec = base85ed.decode(enc)
        assert dec == data


def test_large_data():
    """
    Test with larger data
    """
    data = bytes(range(256)) * 100
    enc = base85ed.encode(data)
    dec = base85ed.decode(enc)
    assert dec == data