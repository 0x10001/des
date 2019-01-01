#!/usr/bin/env python
# encoding: utf-8

"""
   @author: Eric Wong
  @license: MIT Licence
  @contact: ericwong@zju.edu.cn
     @file: base.py
     @time: 2018-12-23 20:30
"""

import struct

from .compatibility import number_type, iter_range
from .core import derive_keys, encode_block


class DesKey(object):
    """A class for encryption using DES Key"""
    def __init__(self, key):
        self.__encryption_key = guard_key(key)
        self.__decryption_key = self.__encryption_key[::-1]
        self.__key = key

    def encrypt(self, message, initial=None, padding=False):
        """Encrypts the message with the key object.

        :param message: {bytes} The message to be encrypted
        :param initial: {union[bytes, int, long, NoneType]} The initial value, using CBC Mode when is not None
        :param padding: {any} Uses PKCS5 Padding when TRUTHY
        :return: {bytes} Encrypted bytes
        """
        return handle(message, self.__encryption_key, initial, padding, 1)

    def decrypt(self, message, initial=None, padding=False):
        """Decrypts the encrypted message with the key object.

        :param message: {bytes} The message to be decrypted
        :param initial: {union[bytes, int, long, NoneType]} The initial value, using CBC Mode when is not None
        :param padding: {any} Uses PKCS5 Padding when TRUTHY
        :return: {bytes} Decrypted bytes
        """
        return handle(message, self.__decryption_key, initial, padding, 0)

    def is_single(self):
        """Tells if the key object is using Single-DES algorithm.

        :return: {bool} True if using DES algorithm or False otherwise
        """
        return len(self.__encryption_key) == 1

    def is_triple(self):
        """Tells if the key object is using Triple-DES algorithm.

        :return: {bool} True if using 3DES algorithm or False otherwise
        """
        return len(self.__encryption_key) == 3

    def __hash__(self):
        return hash((self.__class__, self.__encryption_key))


def encode(block, key, encryption):
    for k in key:
        block = encode_block(block, k, encryption)
        encryption = not encryption

    return block


def guard_key(key):
    if isinstance(key, bytearray):
        key = bytes(key)

    assert isinstance(key, bytes), "The key should be `bytes` or `bytearray`"
    assert len(key) in (8, 16, 24), "The key should be of length 8, 16, or 24"

    k0, k1, k2 = key[:8], key[8:16], key[16:]
    if k1 == k2:
        return tuple(derive_keys(k0)),

    k2 = k2 or k0
    if k1 == k0:
        return tuple(derive_keys(k2)),

    return tuple(tuple(derive_keys(k)) for k in (k0, k1, k2))


def guard_message(message, padding, encryption):
    assert isinstance(message, bytes), "The message should be bytes"
    length = len(message)
    if encryption and padding:
        return message.ljust(length + 8 >> 3 << 3, bytes((8 - (length & 7), )))

    assert length & 7 == 0, (
        "The length of the message should be divisible by 8"
        "(or set `padding` to `True` in encryption mode)"
    )
    return message


def guard_initial(initial):
    if initial is not None:
        if isinstance(initial, bytearray):
            initial = bytes(initial)
        if isinstance(initial, bytes):
            assert len(initial) & 7 == 0, "The initial value should be of length 8(as `bytes` or `bytearray`)"
            return struct.unpack(">Q", initial)[0]
        assert isinstance(initial, number_type), "The initial value should be an integer or bytes object"
        assert -1 < initial < 1 << 32, "The initial value should be in range [0, 2**32) (as an integer)"
    return initial


def handle(message, key, initial, padding, encryption):
    message = guard_message(message, padding, encryption)
    initial = guard_initial(initial)

    blocks = (struct.unpack(">Q", message[i: i + 8])[0] for i in iter_range(0, len(message), 8))

    if initial is None:
        # ECB
        encoded_blocks = ecb(blocks, key, encryption)
    else:
        # CBC
        encoded_blocks = cbc(blocks, key, initial, encryption)

    ret = b"".join(struct.pack(">Q", block) for block in encoded_blocks)
    return ret[:-ord(ret[-1:])] if not encryption and padding else ret


def ecb(blocks, key, encryption):
    for block in blocks:
        yield encode(block, key, encryption)


def cbc(blocks, key, initial, encryption):
    if encryption:
        for block in blocks:
            initial = encode(block ^ initial, key, encryption)
            yield initial
    else:
        for block in blocks:
            initial, block = block, initial ^ encode(block, key, encryption)
            yield block
