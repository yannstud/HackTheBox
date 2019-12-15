#!/bin/bash

while true; do
inotifywait -m -r ./ && echo "gotcha" > file.txt
done
