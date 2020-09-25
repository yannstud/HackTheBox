# Worker

on the nmap we can discover the Subversion port 
after install the svn package 
```
sudo apt install subversion
```
we can download the github repo 
```
svn checkout svn://10.10.10.203:3690
```
from that we can see we need to add the 
	- lens.worker.htb
	- dimension.worker.htb

at our /etc/hosts to see the pages 
---- rabbit hole ----

```
svn checkout -r 2 svn://10.10.10.203:3690
```
```
cat deploy.ps1 
$user = "nathen" 
$plain = "wendel98"
```


