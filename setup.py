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

def run_command(command, retries=3):
    for _ in range(retries):
        if os.system(command) == 0:
            return True
    return False

if run_command("sudo apt update"):
    run_command("sudo apt -y dist-upgrade")
    run_command("sudo apt clean")
    run_command("sudo pip3 install --break-system-packages -U pip")
    run_command("sudo apt-get install -y python-dev python3-pip libfreetype6-dev libjpeg-dev build-essential")
    run_command("sudo -H pip3 install --break-system-packages --upgrade luma.oled")
    run_command("sudo apt-get install -y i2c-tools")
    run_command("sudo apt-get install -y python3-smbus")
    run_command("sudo pip3 install --break-system-packages icm20948")
    run_command("sudo pip3 install --break-system-packages flask")
    run_command("sudo pip3 install --break-system-packages flask_cors")
    run_command("sudo pip3 install --break-system-packages websockets")

try:
    replace_num("/boot/config.txt",'#dtparam=i2c_arm=on','dtparam=i2c_arm=on')
except:
    print('Failed to update /boot/config.txt for i2c_arm=on')

try:
    replace_num("/boot/config.txt",'[all]','[all]\ngpu_mem=128')
except:
    print('Failed to update /boot/config.txt for gpu_mem=128')

try:
    replace_num("/boot/config.txt",'camera_auto_detect=1','#camera_auto_detect=1\nstart_x=1')
except:
    print('Failed to update /boot/config.txt for camera_auto_detect=1')

try:
    replace_num("/boot/config.txt",'camera_auto_detect=1','#camera_auto_detect=1')
except:
    print('Failed to update /boot/config.txt for camera_auto_detect=1')

# Install OpenCV
if not run_command("sudo pip3 install --break-system-packages opencv-contrib-python==3.4.11.45"):
    run_command("sudo pip3 install --break-system-packages -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple opencv-contrib-python==3.4.11.45")

# Install required dependencies for numpy
run_command("sudo apt-get install -y gfortran libopenblas-dev liblapack-dev")

# Uninstall and reinstall numpy
if run_command("sudo pip3 uninstall -y numpy"):
    if not run_command("sudo pip3 install --break-system-packages numpy==1.21 --only-binary=:all:"):
        run_command("sudo pip3 install --break-system-packages -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple numpy==1.21")

run_command("sudo apt-get -y install libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev")
if not run_command("sudo pip3 install --break-system-packages imutils zmq pybase64 psutil"):
    run_command("sudo pip3 install --break-system-packages -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple imutils zmq pybase64 psutil")

run_command("sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq")
run_command("sudo pip3 install --break-system-packages pi-ina219")

if not os.path.exists(os.path.join(thisPath, '..', 'create_ap')):
    if run_command(f"cd {thisPath} && cd .. && sudo git clone https://github.com/oblique/create_ap"):
        run_command(f"cd {thisPath} && cd .. && cd create_ap && sudo make install")

replace_num('/etc/rc.local','exit 0',f'cd {thisPath} && sudo python3 webServer.py &\nexit 0')

print('Completed!')
os.system("sudo reboot")
