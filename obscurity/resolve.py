#!/usr/bin/env python3
import itertools, re, string, sys

def decrypt(text, key):
    keylen = len(key)
    keyPos = 0
    decrypted = ""
    try:
        for x in text:
            keyChr = key[keyPos]
            newChr = ord(x)
            newChr = chr((newChr - ord(keyChr)) % 255)
            decrypted += newChr
            keyPos += 1
            keyPos = keyPos % keylen
    except Exception as e:
        print("[!] Error {}".format(key))

    return decrypted

fc = open("check.txt")
check = fc.read()
fo = open("out.txt")
out = fo.read()
password = decrypt(out, check)
print("[!] decrypt key: {}".format(password))
fp = open("passwordreminder.txt")
passcrypt = fp.read()
print("[!] Password: {}".format(decrypt(passcrypt, password)))
