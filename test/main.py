#!/usr/bin/env python
# encoding: utf-8

"""
   @author: Eric Wong
  @license: MIT Licence
  @contact: ericwong@zju.edu.cn
     @file: main.py
     @time: 2018-12-23 22:31
"""

from unittest import main, TestCase

from des import DesKey

try:
    bytes.fromhex
except AttributeError:
    def h2b(byte_string):
        return bytes(bytearray.fromhex(byte_string))
else:
    def h2b(byte_string):
        return bytes.fromhex(byte_string)


class DesTest(TestCase):
    single_key = DesKey(h2b("0123456789abcdef"))
    triple_key = DesKey(h2b("0123456789abcdeffedcba9876543210"))

    def test_length(self):
        self.assertTrue(self.single_key.is_single())
        self.assertFalse(self.single_key.is_triple())
        self.assertFalse(self.triple_key.is_single())
        self.assertTrue(self.triple_key.is_triple())

    def test_ecb_single(self):
        key = self.single_key
        plain_text = b"hi another world"
        cipher_text = h2b("2d3820d2963f9706ee8b812d03e3a91a")
        self.assertEqual(cipher_text, key.encrypt(plain_text))
        self.assertEqual(plain_text, key.decrypt(cipher_text))

    def test_ecb_triple(self):
        key = self.triple_key
        plain_text = b"hi another world"
        cipher_text = h2b("4938a7bd7e8599465fbef201d341cfa8")
        self.assertEqual(cipher_text, key.encrypt(plain_text))
        self.assertEqual(plain_text, key.decrypt(cipher_text))

    def test_cbc_single(self):
        key = self.single_key
        plain_text = b"hi another world"
        cipher_text = h2b("2d3820d2963f970621d36cb1e97bca5c")
        self.assertEqual(cipher_text, key.encrypt(plain_text, initial=0))
        self.assertEqual(plain_text, key.decrypt(cipher_text, initial=0))

    def test_cbc_triple(self):
        key = self.triple_key
        plain_text = b"hi another world"
        cipher_text = h2b("4938a7bd7e859946f2bae11bb8b65bc7")
        self.assertEqual(cipher_text, key.encrypt(plain_text, initial=0))
        self.assertEqual(plain_text, key.decrypt(cipher_text, initial=0))

    def test_pcks5(self):
        key = self.single_key
        plain_text = b"hello world"
        cipher_text = h2b("1f797e16614dab0a6acd31ea6fbcdc6b")
        self.assertEqual(cipher_text, key.encrypt(plain_text, padding=True))
        self.assertEqual(plain_text, key.decrypt(cipher_text, padding=True))

    def test_pcks5_extra(self):
        key = self.triple_key
        plain_text = b"hi another world"
        cipher_text = h2b("4938a7bd7e8599465fbef201d341cfa82e24eeb85aef49ae")
        self.assertEqual(cipher_text, key.encrypt(plain_text, padding=True))
        self.assertEqual(plain_text, key.decrypt(cipher_text, padding=True))


if __name__ == "__main__":
    main()
