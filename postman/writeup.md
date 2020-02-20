# Postman
## User
nmap nous montre plusieurs port mais un est interessant: Redis
```
https://packetstormsecurity.com/files/134200/Redis-Remote-Command-Execution.html
```
on se rends compte quon peux se connecter a redis sans username password on va en profiter pour mettre un autorized_keys dans le dossier /var/lib/redis/.ssh

puis se co en ssh.

d'ici on se rends compte du fichier id_rsa.bak qu'on peux trouver dans /opt/

un coup de ssh2john -> john nous donne : computer2008

on peux se connecter as Matt grace a su avec le password computer2008

## Root

l'enumeration de Lipnpas ne donne rien d'interessant donc on test de se connecter a webmin avec les creds de Matt

on peux se connecter !

on va pouvoir tester les eploits de Webmin, il nous manquais des creds utilisateur 

```
use linux/http/webmin_packageup_rce
```

on remplis les cases et wait de recevoir un shell root :D
