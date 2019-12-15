import os
from shutil import copyfile

i = 1
while i:
    if len(os.listdir('.')) == 1:
        print("Directory is empty")
    else:
        print("Directory is not empty")
        copyfile(os.listdir('./')[1], "/tmp/pass")
        break

