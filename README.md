![version](https://img.shields.io/pypi/v/des.svg) ![license](https://img.shields.io/pypi/l/des.svg)

# DES (Data Encryption Standard)
A pure Python implementation for the famous DES algorithm, supporting Python 2 and 3.

## Installation
Using `pip`:
```bash
$ pip install des 
```

Or manually download the archive and run the command after extracting the stuff inside:
```bash
$ python setup.py install
```

## Usage
Firstly, define a `DesKey` object by passing your encryption / decryption key. The key should be of length 8, 16 or 24. The algorithm will be automatically chosen for you.
Note that the key should be written as `bytes` in *Python 3*.
```python
from des import DesKey
key0 = DesKey(b"some key")                  # for DES
key1 = DesKey(b"a key for TRIPLE")          # for 3DES, same as "a key for TRIPLEa key fo"
key2 = DesKey(b"a 24-byte key for TRIPLE")  # for 3DES
key3 = DesKey(b"1234567812345678REAL_KEY")  # for DES, same as "REAL_KEY"
```

You may know whether a key is for *DES* or *3DES* algorithm by calling its method `is_single()` or `is_triple()`.
```python
key0.is_single()  # -> True
key1.is_triple()  # -> True
key2.is_single()  # -> False
key3.is_triple()  # -> False
```

Secondly, encrypt messages by calling the method `encrypt()` from the `DesKey` object, or decrypt them by calling `decrypt()`.
Note that the messages should be written as `bytes` in *Python 3*.
```python
key0.encrypt(b"any long message")  # -> b"\x14\xfa\xc2 '\x00{\xa9\xdc;\x9dq\xcbr\x87Q"
```

By default, *ECB Mode* is used. You may enable *CBC Mode* by passing the argument `initial`, as the *Initial Value*.
The argument may be either a `bytes` object of length 8 or an integer using *big-endian*. 
```python
key0.encrypt(b"any long message", initial=0)        # -> b"\x14\xfa\xc2 '\x00{\xa9\xb2\xa5\xa7\xfb#\x86\xc5\x9b"
key0.encrypt(b"any long message", initial=b"\0"*8)  # same as above
```

The *DES* algorithm requires the message to be of any length that is a multiple of 8.
By default, the length of the message to encrypt / decrypt is assured by users.
You may choose to turn on *PKCS5 Padding Mode*(by passing the argument `padding` with a TRUTHY value), telling Python to do the padding before encryption for you.
```python
key0.encrypt(b"abc", padding=True)  # -> b"%\xd1KU\x8b_A\xa6"
```

While in decryption with *PKCS5 Padding*, the length of the message is still required to be a multiple of 8. But after decryption, Python will throw the padding characters away. 
```python
key0.decrypt(b"%\xd1KU\x8b_A\xa6", padding=True)  # -> b"abc"
```

## Note
Because DES keys are 56 bits and the input key to this algorithm is 8, 16 or 24 bytes, this implementation ignores the least significant bit of each key byte.
