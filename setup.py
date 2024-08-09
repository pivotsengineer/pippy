#!/usr/bin/python3
# File name   : setup.py for PIPPY
# Date        : 2020/11/24

import os
import time
import re

curpath = os.path.realpath(__file__)
thisPath = os.path.dirname(curpath)

def replace_num(file,initial,new_num):  
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)

for x in range(1,4):
	if os.system("sudo apt update") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt -y dist-upgrade") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt clean") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y python3-dev python3-pip libfreetype6-dev libjpeg-dev build-essential") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y python3-flask python3-flask-cors python3-websockets") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y python3-opencv python3-numpy python3-imutils python3-zmq python3-psutil") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y python3-smbus i2c-tools") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y python3-pi-ina219") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq") == 0:
		break

for x in range(1,4):
	if os.system("cd " + thisPath + " && cd .. && sudo git clone https://github.com/oblique/create_ap") == 0:
		break

try:
	os.system("cd " + thisPath + " && cd .. && cd create_ap && sudo make install")
except:
	pass

replace_num('/etc/rc.local','exit 0','cd '+thisPath+' && sudo python3 webServer.py &\nexit 0')

print('Completed!')

os.system("sudo reboot")
